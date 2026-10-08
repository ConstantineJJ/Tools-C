# Visual, runtime and performance evidence

Read for L3/L4 checks or a comparison whose presentation could change the conclusion.

For 3D character delivery, obtain fixed high_45 and low_45 images along
with front/side/back orthographic and three-quarter views. The two 45-degree
angles diagnose volume/contacts rather than independently measuring head,
feet or leg length; a perspective camera can exaggerate nearest parts and
even orthographic obliques foreshorten projected lengths. Never let a single
oblique view trigger destructive proportion adjustment. Protect approved
zones and compare user MUST_FIX/DO_NOT_REINTERPRET marks on aligned images.
A final acceptance receipt may be structurally complete while visually
wrong; named reviewer must inspect images.

For before/after visuals, hold camera, projection, framing, lighting, pose, frame and material state fixed. Inspect the affected views and the target-engine appearance. For animation, use playback plus contact/extreme and loop frames; for deformation, neutral and relevant bend/twist poses. Restore temporary cameras, poses and debug settings.

For runtime, assert the requested behavior in the actual scene/bridge/input path and one affected neighboring instance or case. An import or process exit code alone is not a runtime assertion. Record the exact command, version, output marker, errors and limitations.

For performance, use the same workload, viewport and warm-up. Compare frame time rather than relying only on subjective smoothness; include GPU load and temperature when significant graphics work could change hardware stress. Report unavailable measurements as SKIP.

Anti-degradation questions depend on the task: requested result, another view/asset, silhouette, topology, deformation, animation, runtime stability and complexity. Mark irrelevant questions as inapplicable only when their relationship to the change is clear. Do not turn the checklist into unrelated full-project testing.
