# Roadmap

This file records work intentionally deferred from active Conductor tracks. Items here are
planning commitments, not current development tasks, implementation authorization, or evidence
that a platform has passed qualification. There is no target date until the maintainer reprioritizes
the work.

## Cross-platform engineering qualification

Current engineering development is focused on macOS. The following work is deferred:

- Install and execute the source-bound Linux x86_64 audit lock under Python 3.15.1.
- Qualify the engineering matrix on Linux and Windows and retain hosted results for each platform.
- Diagnose and repair non-macOS hosted-runner failures using their actual annotations.
- Verify packaging, dependency markers, paths, encodings and scientific reproduction behavior on
  supported non-macOS platforms.
- Reconsider when cross-platform qualification should return to active tracks.

The existing workflow definitions and repository checks remain unchanged. They may still execute
on non-macOS runners; this roadmap does not waive their failures, assert success, or change branch
protection. Any returned work must use current `main`, preserve in-flight work, and record actual
platform-specific verification.
