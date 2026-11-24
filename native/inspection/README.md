# Conditional inspection scenarios

The opt-in M2a adapter runs a locked Rust executable for either a border-seizure or retail-inspection scenario. Build and test it with Rust 1.99.1.

```bash
cargo build --locked --manifest-path native/inspection/Cargo.toml
cargo test --locked --manifest-path native/inspection/Cargo.toml
```

Pass the executable, versioned JSON request and matched observations to `tobac.strategic_inspection.run_inspection_scenario`. Set the expected channel, scenario ID and calibration digest on `InspectionObservations` from the reviewed application case. The wrapper checks that context against the native receipt before conditioning the ratios. The fiscal packet must match the scenario and the declared currency, price year and resource basis. Dapane supplies the enforcement resource cost and Paignia projects the admitted detection interval. The receipt retains exact strategic bounds, fiscal provenance and the full paired-draw identity.

The conditional M2a projection requires a source-identified calibration of the game output to lawful-to-illicit switching among continuing consumers within the same product, population, geography and observation period. Empirical calibration remains pending. The regression fixture uses synthetic inputs and fiscal bytes from Dapane at `d02095d`. [Dapane fixture](https://github.com/edithatogo/dapane/blob/d02095d9bf7e89c6fc00805c4bc484a3ead3e33b/adapters/decision_draws/fixtures/fiscal-nz-synthetic.json)

## Voiage handoff

Use `InspectionDecisionDraw` to supply each joint continuing and lawful consumption outcome as exact fractions, its native scenario result, and an explicit prior weight. Call `prepare_inspection_paired_draws` with the application's valuation function and a shared net-benefit unit. It checks each joint outcome against the original observation intervals and exact native switching support before calling the valuation. The valuation returns net benefits for the fiscal strategy and its comparator, in that order.

Convert the returned rows to an Arrow table and pass the table, dataset ID, and strategy IDs to Voiage's `paired_draw_bundle` with `weight_field="weight"`. Use the returned perspective and subgroup with the application's censored acquisition stages. Keep each coherent candidate model together when reporting a range across a finite set of models. The result retains the Dapane draw-set digest and the original fiscal keys, including replication IDs.

Run the installed-consumer check with a Python 3.15.2 environment containing the candidate Tobac wheel, PyArrow and Voiage 3.1.0.

```bash
"$replay_python" -I native/inspection/tests/voiage_handoff.py native/inspection/target/debug/tobac-inspection
```

The check uses the same assay and valuation rules for both channels. It verifies that a tighter native support excludes an otherwise admissible model and changes the finite-model EVSI range from `[0, 1/2]` to `[0, 0]`. With the same paired net benefits and a declared prior-weight interval, the comparator is the sole interval-undominated strategy after narrowing.
