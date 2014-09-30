import bge
from mathutils import Matrix


#Generate an orientation with one definite (locked) axis
# and another axis aligned to a vector as close as possible
# without breaking the locked axis. Default Z locked with Y tracking.
def vectrack(v0, v1, lock_axis=2, track_axis=1):
	if lock_axis == track_axis:
		print("vectrack(): Locked axis can't be the same as the tracking axis.")
		return Matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]])

	lock = v0.normalized()
	track = v1.normalized()
	#Gimbal lock! (Vectors are either identical or the inverse of each other)
	if abs(lock.dot(track)) == 1:
		return Matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]])

	other = track.cross(lock).normalized()
	track = lock.cross(other)

	#No idea where I pulled this operation from.
	other_axis = 3 - (lock_axis + track_axis)

	#Or this one. I must have hammerspace!
	if not (lock_axis - 1) % 3 == track_axis:
		other = -other

	r = Matrix([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
	r.col[lock_axis] = lock
	r.col[track_axis] = track
	r.col[other_axis] = other
	return r


def drawMat(mat, pos):
	bge.render.drawLine(pos, pos + mat[0], [1, 0, 0])
	bge.render.drawLine(pos, pos + mat[1], [0, 1, 0])
	bge.render.drawLine(pos, pos + mat[2], [0, 0, 1])


def drawVec(vec, pos):
	bge.render.drawLine(pos, pos + vec, [1, 1, 1])


def limit(value, lower, upper):
	return max(min(value, upper), lower)


def towards(current, target, amount):
	if current > target:
		return current - min(abs(target - current), amount)
	elif current < target:
		return current + min(abs(target - current), amount)
	return current


def sign(the_number):
	if the_number < 0:
		return -1.0
	elif the_number > 0:
		return 1.0
	raise ValueError


def vecplaneproject(point, nor):
	nor = nor.normalized()  # Copy the normal.
	return point - nor.dot(point) * nor


def vecproject(point, nor):
	nor = nor.normalized()
	return nor * nor.dot(point)


def dualplanelimit(pos, dir, radius):
	diff = dir.dot(pos)
	if diff > +radius:
		pos -= dir * (diff - radius)
	if diff < -radius:
		pos -= dir * (radius + diff)
	return pos


def lerp(p0, p1, t):
	return p0 + (p1 - p0) * t
