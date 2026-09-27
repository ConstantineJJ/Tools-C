# Visual, runtime and performance evidence

Read for L3/L4 checks or a comparison whose presentation could change the conclusion.

For before/after visuals, hold camera, projection, framing, lighting, pose, frame and material state fixed. Inspect the affected views and the target-engine appearance. For animation, use playback plus contact/extreme and loop frames; for deformation, neutral and relevant bend/twist poses. Restore temporary cameras, poses and debug settings.

For runtime, assert the requested behavior in the actual scene/bridge/input path and one affected neighboring instance or case. An import or process exit code alone is not a runtime assertion. Record the exact command, version, output marker, errors and limitations.

For performance, use the same workload, viewport and warm-up. Compare frame time rather than relying only on subjective smoothness; include GPU load and temperature when significant graphics work could change hardware stress. Report unavailable measurements as SKIP.

Anti-degradation questions depend on the task: requested result, another view/asset, silhouette, topology, deformation, animation, runtime stability and complexity. Mark irrelevant questions as inapplicable only when their relationship to the change is clear. Do not turn the checklist into unrelated full-project testing.
