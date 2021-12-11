import java.io.File
import kotlin.math.abs
import kotlin.math.min

val crabs = File("7.in").readLines().first().let { l -> l.split(",").map(String::toInt) }.groupingBy { it }.eachCount()
    .toSortedMap()

val distances = (crabs.keys.first()..crabs.keys.last()).map { pos ->
    crabs.entries.map { (groupPos, groupCount) ->
        val dist = abs(groupPos - pos)
        groupCount * ((dist + 1) * dist) / 2
    }.sum()
}

distances.minByOrNull { it }