use std::process::{Command, Output, Stdio};

use serde_json::{Value, json};

const FISCAL_FIXTURE: &str = include_str!("fixtures/fiscal-nz-synthetic.json");

fn ratio(numerator: i64, denominator: i64) -> Value {
    json!({"numerator": numerator.to_string(), "denominator": denominator.to_string()})
}

fn request(channel: &str) -> Value {
    let scenario_id = format!("synthetic-{channel}");
    let mut fiscal: Value = serde_json::from_str(FISCAL_FIXTURE).unwrap();
    fiscal["key"]["scenario_id"] = json!(scenario_id);
    json!({
        "schema_version": "tobac-inspection/0.1",
        "scope": {
            "channel": channel,
            "scenario_id": scenario_id,
            "product": "synthetic product",
            "observations": {
                "geography": "NZ",
                "population": "synthetic continuing consumers",
                "start": "2026-01-01",
                "end": "2026-12-31",
                "unit": "baseline share"
            },
            "switching_measure": "evasion_among_continuing_consumers",
            "calibration_sha256": "sha256:a9fb29cdbc9b11c5bd82087030b7a8f91f656f0389401691445d0a3bf343ea75"
        },
        "inspector_valuation": {
            "currency": "NZD",
            "price_year": 2026,
            "resource_basis": "public_expenditure"
        },
        "fiscal_packet": fiscal,
        "undetected_harm": ratio(64, 1),
        "evasion_gain": ratio(1, 1),
        "detected_loss": ratio(3, 1),
        "detection": {"lower": ratio(1, 2), "upper": ratio(1, 1)}
    })
}

fn execute(request: &Value) -> Output {
    let mut child = Command::new(env!("CARGO_BIN_EXE_tobac-inspection"))
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()
        .unwrap();
    serde_json::to_writer(child.stdin.take().unwrap(), request).unwrap();
    child.wait_with_output().unwrap()
}

#[test]
fn projects_both_channels_from_the_valued_cost_and_retains_draw_identity() {
    for channel in ["border_seizure", "retail_inspection"] {
        let request = request(channel);
        let output = execute(&request);
        assert!(
            output.status.success(),
            "{channel}: {}",
            String::from_utf8_lossy(&output.stderr)
        );
        let receipt: Value = serde_json::from_slice(&output.stdout).unwrap();
        assert_eq!(receipt["scope"], request["scope"]);
        assert_eq!(receipt["fiscal"]["key"], request["fiscal_packet"]["key"]);
        assert_eq!(
            receipt["fiscal"]["draw_set_digest"],
            request["fiscal_packet"]["draw_set_digest"]
        );
        assert_eq!(
            receipt["fiscal"]["resources"]["enforcement_resource_cost"],
            ratio(16, 1)
        );
        let shares = json!({"lower": ratio(1, 4), "upper": ratio(1, 2)});
        assert_eq!(receipt["projection"]["inspection"], shares);
        assert_eq!(receipt["projection"]["evasion"], shares);
        assert_eq!(
            receipt["projection"]["inspector_payoff"],
            json!({"lower": ratio(-32, 1), "upper": ratio(-16, 1)})
        );
        assert_eq!(receipt["projection"]["endpoint_gap"], ratio(0, 1));
    }
}

#[test]
fn rejects_fiscal_context_mismatches_and_crossing_detection_regimes() {
    let base = request("retail_inspection");
    for (pointer, replacement, reason) in [
        (
            "/inspector_valuation/currency",
            json!("AUD"),
            "valuation contexts differ",
        ),
        (
            "/fiscal_packet/key/scenario_id",
            json!("another-scenario"),
            "scenario identities differ",
        ),
        ("/detection/lower", ratio(1, 8), "regime"),
    ] {
        let mut request = base.clone();
        *request.pointer_mut(pointer).unwrap() = replacement;
        let output = execute(&request);
        assert!(!output.status.success(), "{pointer}");
        assert!(output.stdout.is_empty(), "{pointer}");
        let stderr = String::from_utf8_lossy(&output.stderr);
        assert!(stderr.contains(reason), "{pointer}: {stderr}");
    }
}
