# Joint topology and pose checks

Read while designing deformation loops or diagnosing a pose failure.

Mark the required joints and motion ranges from the active asset. Elbows and knees need enough surrounding geometry for inside compression and outside stretch; shoulders and hips need flow for multi-axis motion. Wrists, ankles and neck need rotation without severe pinch or unrelated volume pull. Keep rigid armor and accessories separate when that produces cleaner behavior.

Use density for silhouette and bending, not uniform polygon counts. Check normals, mirrored seam, subdivision and highlight flow after retopology. Place poles away from maximum bend and visible highlight paths. A triangle is acceptable where it deforms and shades correctly.

Test neutral plus the relevant extremes: overhead/forward arm, elbow bend, hip flexion, knee bend, twist or face/jaw pose only where the asset uses them. Inspect from front, side and three-quarter as appropriate. Record collapse, twist pinch, spikes, tearing, cloth intersection and shading. Compare the result to the original pose and UV/weight dependencies before accepting the patch.
