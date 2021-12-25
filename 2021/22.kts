import java.io.File
import kotlin.math.abs
import kotlin.math.min
import kotlin.reflect.KProperty1

data class Point3D(
    val x: Long,
    val y: Long,
    val z: Long
)

fun Point3D.trimTo(range: LongRange): Point3D {
    return Point3D(
        maxOf(minOf(x, range.last), range.first),
        maxOf(minOf(y, range.last), range.first),
        maxOf(minOf(z, range.last), range.first)
    )
}

data class Cuboid(
    val a: Point3D,
    val b: Point3D,
    val state: Boolean
) {
    val xRange: LongRange
        get() {
            val (x1, x2) = listOf(a, b).map { it.x }.sorted()
            return x1 until x2
        }

    val yRange: LongRange
        get() {
            val (y1, y2) = listOf(a, b).map { it.y }.sorted()
            return y1 until y2
        }

    val zRange: LongRange
        get() {
            val (z1, z2) = listOf(a, b).map { it.z }.sorted()
            return z1 until z2
        }

    val volume: Long
        get() = abs(a.x - b.x) * abs(a.y - b.y) * abs(a.z - b.z)
}

fun Cuboid.contains(other: Cuboid): Boolean {
    val xR = other.xRange
    val yR = other.yRange
    val zR = other.zRange
    return xRange.let { it.contains(xR.first) && it.contains(xR.last) } &&
        yRange.let { it.contains(yR.first) && it.contains(yR.last) } &&
        zRange.let { it.contains(zR.first) && it.contains(zR.last) }
}

fun Cuboid.overlaps(other: Cuboid): Boolean {
    val altX = (xRange.first <= other.xRange.last) && (xRange.last >= other.xRange.first)
    val altY = (yRange.first <= other.yRange.last) && (yRange.last >= other.yRange.first)
    val altZ = (zRange.first <= other.zRange.last) && (zRange.last >= other.zRange.first)

    return altX && altY && altZ
}

fun Cuboid.axisCutout(left: Long, right: Long, selector: KProperty1<Point3D, Long>): List<Pair<Cuboid, Boolean>> {
    val thresholds: MutableMap<Long, Boolean> = sortedMapOf()
    thresholds[selector.invoke(a)] = false
    thresholds[selector.invoke(b)] = false

    val (aS, bS) = listOf(selector.invoke(a), selector.invoke(b)).sorted()
    val (first, second) = listOf(left, right).sorted()
    val firstTruncated = maxOf(aS, first)
    val secondTruncated = min(bS, second)

    thresholds[firstTruncated] = true
    thresholds[secondTruncated] = true

    val g = listOf(true, false).iterator()
    return thresholds.entries.zipWithNext { curr, next ->
        val (startValue, isCutout) = curr
        val (endValue, _) = next

        when (selector) {
            Point3D::x -> Cuboid(
                a.copy(x = startValue),
                b.copy(x = endValue),
                state
            )
            Point3D::y -> Cuboid(
                a.copy(y = startValue),
                b.copy(y = endValue),
                state
            )
            Point3D::z -> Cuboid(
                a.copy(z = startValue),
                b.copy(z= endValue),
                state
            )
            else -> throw IllegalStateException()
        } to (if (isCutout) {
            g.next()
        } else false)
    }
}

fun Cuboid.carveOut(shape: Cuboid): List<Cuboid> {
    val result = mutableListOf<Cuboid>()

    val (xCarvedOut, xContaining) = axisCutout(shape.a.x, shape.b.x, Point3D::x).partition { !it.second }
    result.addAll(xCarvedOut.map { it.first })

    val (yCarvedOut, yContaining) = xContaining.first().first.axisCutout(shape.a.y, shape.b.y, Point3D::y).partition { !it.second }
    result.addAll(yCarvedOut.map { it.first })

    val (zCarvedOut, _) = yContaining.first().first.axisCutout(shape.a.z, shape.b.z, Point3D::z).partition { !it.second }
    result.addAll(zCarvedOut.map { it.first })

    return result
}

var cuboids: MutableSet<Cuboid> = mutableSetOf()

File("22.in").readLines().map { line ->
    val (command, ranges) = line.split(' ')
    val (x, y, z) = ranges.split(',').map { numRange ->
        val (from, to) = numRange.drop(2).split("..").map(String::toLong)
        from to to
    }

    val cuttingCuboid = Cuboid(
        Point3D(x.first, y.first, z.first),
        Point3D(x.second + 1, y.second + 1, z.second + 1),
        command == "on"
    )

    val newCuboids = mutableSetOf<Cuboid>()
    cuboids.forEach { cuboid ->
        if (cuttingCuboid.contains(cuboid)) {
            // we just throw it away
        } else if (cuboid.overlaps(cuttingCuboid)) {
            cuboid.carveOut(cuttingCuboid).forEach {
                newCuboids.add(it)
            }
        } else {
            newCuboids.add(cuboid)
        }
    }
    newCuboids.add(cuttingCuboid)

    cuboids = newCuboids
}

val range = -51..51
cuboids.filter { it.state }.sumOf { it.volume }