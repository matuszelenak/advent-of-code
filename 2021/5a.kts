import java.io.File
import kotlin.math.abs

fun rrange(from: Int, to: Int) = (if (from > to) (from downTo to) else (from..to)).toList()

fun List<Int>.zzip(other: List<Int>) = (0 until maxOf(this.size, other.size)).map {
    getOrElse(it, { this@zzip.first() }) to other.getOrElse(it, { other.first() })
}

fun iteratePoints(from: Pair<Int, Int>, to: Pair<Int, Int>): List<Pair<Int, Int>> {
    //if (!(from.first == to.first || from.second == to.second)) return emptyList()
    return rrange(from.first, to.first).zzip(rrange(from.second, to.second))
}

val pointOccurences = mutableMapOf<Pair<Int, Int>, Int>().withDefault { 0 }
File("5.in").readLines().map { line ->
    val (from, to) = line.split(" -> ").map {
        val (x, y) = it.split(",").map(String::toInt)
        Pair(x, y)
    }
    iteratePoints(from, to).forEach { pointOccurences[it] = pointOccurences.getValue(it) + 1 }
}

pointOccurences.filter { it.value >= 2 }.count()
