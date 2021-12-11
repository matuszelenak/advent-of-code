import java.io.File

val crabs = File("7.in").readLines().first().let { l -> l.split(",").map(String::toInt) }.groupingBy { it }.eachCount()
    .toSortedMap()

val fuelToPositionFromLeft = mutableMapOf<Int, Int>()
fuelToPositionFromLeft[crabs.keys.first()] = 0

var seenCrabs = 0
var previousCrabPosition: Int = crabs.keys.first()
fuelToPositionFromLeft[crabs.keys.first()]

crabs.entries.forEach { (crabPos, groupSize) ->
    fuelToPositionFromLeft[crabPos] =
        fuelToPositionFromLeft[previousCrabPosition]!! + seenCrabs * (crabPos - previousCrabPosition)

    previousCrabPosition = crabPos
    seenCrabs += groupSize
}


val fuelToPositionFromRight = mutableMapOf<Int, Int>()
fuelToPositionFromRight[crabs.keys.last()] = 0
seenCrabs = 0
previousCrabPosition = crabs.keys.last()
fuelToPositionFromRight[crabs.keys.last()]

crabs.entries.reversed().forEach { (crabPos, groupSize) ->
    fuelToPositionFromRight[crabPos] =
        fuelToPositionFromRight[previousCrabPosition]!! + seenCrabs * (previousCrabPosition - crabPos)

    previousCrabPosition = crabPos
    seenCrabs += groupSize
}

val totalCosts = mutableMapOf<Int, Int>()
fuelToPositionFromLeft.keys.forEach { pos ->
    totalCosts[pos] = fuelToPositionFromRight[pos]!! + fuelToPositionFromLeft[pos]!!
}

totalCosts.entries.minByOrNull { it.value }
