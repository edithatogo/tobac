//! App-owned inspection projection with separate fiscal and strategic outputs.

use std::error::Error;
use std::fmt::Write as _;
use std::io::{self, Read, Write};
use std::process::ExitCode;

use dapane_decision_fiscal::fiscal::evaluate_fiscal_json;
use paignia_solve::{
    InspectionParameters, InspectionRatio, RatioBounds, inspection_detection_projection,
};
use serde::{Deserialize, Serialize};
use serde_json::Value;
use serde_json::value::RawValue;
use sha2::{Digest, Sha256};

const MAX_REQUEST: u64 = 5 << 20;
const DAPANE_REVISION: &str = "d02095d9bf7e89c6fc00805c4bc484a3ead3e33b";
const PAIGNIA_REVISION: &str = "a09c3f8359363b228154c9e07af20a36bf0dcd4e";

#[derive(Deserialize)]
enum RequestSchema {
    #[serde(rename = "tobac-inspection/0.1")]
    V1,
}

#[derive(Deserialize, Serialize)]
#[serde(rename_all = "snake_case")]
enum Channel {
    BorderSeizure,
    RetailInspection,
}

#[derive(Deserialize, Serialize)]
#[serde(deny_unknown_fields)]
struct ObservationScope {
    geography: String,
    population: String,
    start: String,
    end: String,
    unit: String,
}

#[derive(Deserialize, Serialize)]
#[serde(rename_all = "snake_case")]
enum SwitchingMeasure {
    EvasionAmongContinuingConsumers,
}

#[derive(Deserialize, Serialize)]
#[serde(deny_unknown_fields)]
struct Scope {
    channel: Channel,
    scenario_id: String,
    product: String,
    observations: ObservationScope,
    switching_measure: SwitchingMeasure,
    calibration_sha256: String,
}

impl Scope {
    fn validate(&self) -> Result<(), Box<dyn Error>> {
        for label in [
            &self.scenario_id,
            &self.product,
            &self.observations.geography,
            &self.observations.population,
            &self.observations.start,
            &self.observations.end,
            &self.observations.unit,
        ] {
            if label.is_empty()
                || label.len() > 128
                || label.trim() != label
                || label.chars().any(char::is_control)
            {
                return Err("scenario scope contains an invalid identity".into());
            }
        }
        let digest = self.calibration_sha256.strip_prefix("sha256:");
        if !digest.is_some_and(|value| {
            value.len() == 64
                && value
                    .bytes()
                    .all(|byte| byte.is_ascii_digit() || matches!(byte, b'a'..=b'f'))
        }) {
            return Err("switching calibration must identify its source by SHA-256".into());
        }
        Ok(())
    }
}

#[derive(Deserialize, Serialize)]
#[serde(deny_unknown_fields)]
struct Exact {
    numerator: String,
    denominator: String,
}

impl Exact {
    fn ratio(&self) -> Result<InspectionRatio, Box<dyn Error>> {
        let numerator: i64 = self.numerator.parse()?;
        let denominator: i64 = self.denominator.parse()?;
        if numerator.to_string() != self.numerator
            || denominator <= 0
            || denominator.to_string() != self.denominator
        {
            return Err("expected a canonical rational with a positive denominator".into());
        }
        Ok(InspectionRatio::new(numerator, denominator)?)
    }
}

impl From<InspectionRatio> for Exact {
    fn from(value: InspectionRatio) -> Self {
        Self {
            numerator: value.numerator().to_string(),
            denominator: value.denominator().to_string(),
        }
    }
}

#[derive(Deserialize, Serialize)]
#[serde(deny_unknown_fields)]
struct Bounds {
    lower: Exact,
    upper: Exact,
}

impl From<RatioBounds> for Bounds {
    fn from(value: RatioBounds) -> Self {
        Self {
            lower: value.lower.into(),
            upper: value.upper.into(),
        }
    }
}

#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
struct ValuationContext {
    currency: String,
    price_year: u16,
    resource_basis: String,
}

#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
struct Request {
    schema_version: RequestSchema,
    scope: Scope,
    inspector_valuation: ValuationContext,
    fiscal_packet: Box<RawValue>,
    undetected_harm: Exact,
    evasion_gain: Exact,
    detected_loss: Exact,
    detection: Bounds,
}

#[derive(Deserialize, Serialize)]
struct Resources {
    enforcement_resource_cost: Exact,
}

#[derive(Deserialize, Serialize)]
struct FiscalSummary {
    schema_version: String,
    method_version: String,
    key: Value,
    comparator_strategy_id: String,
    draw_set_digest: String,
    jurisdiction: String,
    currency: String,
    price_year: u16,
    perspective: String,
    resource_basis: String,
    input_digest: String,
    output_digest: String,
    resources: Resources,
    net_monetary_benefit: Option<Exact>,
    net_public_outlay: Option<Exact>,
}

fn project(input: &[u8]) -> Result<Value, Box<dyn Error>> {
    let request: Request = serde_json::from_slice(input)?;
    let RequestSchema::V1 = request.schema_version;
    request.scope.validate()?;

    let fiscal: FiscalSummary =
        serde_json::from_str(&evaluate_fiscal_json(request.fiscal_packet.get())?)?;
    if fiscal.key.get("scenario_id").and_then(Value::as_str)
        != Some(request.scope.scenario_id.as_str())
    {
        return Err("fiscal and inspection scenario identities differ".into());
    }
    if fiscal.currency != request.inspector_valuation.currency
        || fiscal.price_year != request.inspector_valuation.price_year
        || fiscal.resource_basis != request.inspector_valuation.resource_basis
    {
        return Err("fiscal and inspection valuation contexts differ".into());
    }

    let game = InspectionParameters::try_new(
        fiscal.resources.enforcement_resource_cost.ratio()?,
        request.undetected_harm.ratio()?,
        request.evasion_gain.ratio()?,
        request.detected_loss.ratio()?,
    )?;
    let bounds = inspection_detection_projection(
        game,
        request.detection.lower.ratio()?,
        request.detection.upper.ratio()?,
    )?;
    let mut input_sha256 = String::from("sha256:");
    for byte in Sha256::digest(input) {
        write!(input_sha256, "{byte:02x}")?;
    }
    Ok(serde_json::json!({
        "schema_version": "tobac-inspection-result/0.1",
        "method": "paignia_detection_nash_projection",
        "paignia_revision": PAIGNIA_REVISION,
        "dapane_revision": DAPANE_REVISION,
        "input_sha256": input_sha256,
        "scope": request.scope,
        "fiscal": fiscal,
        "projection": {
            "inspection": Bounds::from(bounds.inspect),
            "evasion": Bounds::from(bounds.evade),
            "inspector_payoff": Bounds::from(bounds.leader),
            "counterparty_payoff": Bounds::from(bounds.follower),
            "endpoint_gap": Exact::from(bounds.endpoint_gap),
        },
    }))
}

fn run() -> Result<(), Box<dyn Error>> {
    let mut input = Vec::new();
    io::stdin()
        .lock()
        .take(MAX_REQUEST + 1)
        .read_to_end(&mut input)?;
    if input.len() as u64 > MAX_REQUEST {
        return Err("inspection request exceeds the byte limit".into());
    }
    let output = serde_json::to_vec(&project(&input)?)?;
    let mut stdout = io::stdout().lock();
    stdout.write_all(&output)?;
    stdout.write_all(b"\n")?;
    Ok(())
}

fn main() -> ExitCode {
    match run() {
        Ok(()) => ExitCode::SUCCESS,
        Err(error) => {
            eprintln!("Inspection request failed ({error})");
            ExitCode::FAILURE
        }
    }
}
