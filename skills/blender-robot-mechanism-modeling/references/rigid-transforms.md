# Rigid transforms and shared data

Read dependency state explicitly before deriving world/local transforms. After
creation, parenting or scripted placement, update the view layer/dependency graph
before copying evaluated matrices. Prefer an explicit transform frame to copying
a newly created object's potentially stale `matrix_local`.

For a child's desired world placement `W` and parent world matrix `P`, a clear
convention is identity parent inverse plus local basis `P.inverted() @ W`; for
panel-local detail use the panel-local frame deliberately. Preserve `W` if
reparenting should not move the child. Record whether code consumes local or world
coordinates, check matrix inversion/scale assumptions, then verify the resulting
world placement and hierarchy after dependency update. Do not mix both conventions.

Before modifying vertices, list users of the mesh datablock. For a rigid move,
change object matrices rather than source vertices. For a prototype correction,
edit each distinct mesh once. For one instance's shape, make its mesh independent
first and record the exception. Stable registry IDs/roles select owned geometry;
substring name matches may locate candidates but cannot determine edit scope.

Choose repeated bolts/rings/panels as linked data while identical; preserve pivots
and module boundaries. Wear batching must not combine articulated parts merely to
reduce object count. Snapshot prototype identity and instance transforms before
edits, then compare intended and unaffected users afterward.

For destructive batch operations, collect IDs/group membership before deletion,
write completed-stage checkpoints and reacquire remaining objects by stable ID.
Do not retain references to Blender objects after removal or retry an already
completed join/edit blindly after a timeout. Use the existing bounded operation
tools if available; this specialist does not invent a new job framework.

Fresh-load verification should activate/update every scene/view layer relevant
to protected-object comparisons before reading matrices. Lazy inactive matrices
can produce misleading unchanged-object fingerprint failures.
