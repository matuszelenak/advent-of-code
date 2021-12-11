import java.io.File

val cache = mutableMapOf<Int, Long>(0 to 0)

fun offsprings(daysLeft: Int): Long {
    cache[daysLeft]?.let { return it }
    val direct = (1L + (daysLeft - 1) / 7L)
    val indirect = (1..direct).map {
        offsprings(daysLeft - ((it.toInt() - 1) * 7 + 9))
    }.sum()
    return (direct + indirect).also { cache[daysLeft] = it }
}

File("6.in").readLines().first().split(",").map { 1L + offsprings(256 - it.toInt()) }.sum()
