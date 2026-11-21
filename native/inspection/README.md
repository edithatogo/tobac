# Conditional inspection scenarios


The opt-in M2a adapter runs a locked Rust executable for either a border-seizure or retail-inspection scenario. Build and test it with Rust 1.99.1.

```bash
cargo build --locked --manifest-path native/inspection/Cargo.toml
cargo test --locked --manifest-path native/inspection/Cargo.toml
```

Pass the executable, versioned JSON request and matched observations to `tobac.strategic_inspection.run_inspection_scenario`. The fiscal packet must match the scenario and the declared currency, price year and resource basis. Dapane supplies the enforcement resource cost and Paignia projects the admitted detection interval. The receipt retains exact strategic bounds, fiscal provenance and the full paired-draw identity.

The conditional M2a projection requires a source-identified calibration of the game output to lawful-to-illicit switching among continuing consumers within the same product, population, geography and observation period. The supplied regression fixture is synthetic. Its fiscal bytes are copied from Dapane at `d02095d`. The tests assign each channel its own scenario ID. Empirical calibration and qualified application execution with Voiage remain open. [Dapane fixture](https://github.com/edithatogo/dapane/blob/d02095d9bf7e89c6fc00805c4bc484a3ead3e33b/adapters/decision_draws/fixtures/fiscal-nz-synthetic.json)
