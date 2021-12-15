import java.io.File
import kotlin.system.exitProcess

val original = File("15.in").readLines().map { line -> line.map { it.toString().toInt() } }

val enlarge = 5

val grid = mutableListOf<MutableList<Int>>()
repeat(original.size * enlarge) {
    grid.add(mutableListOf())
    repeat(original[0].size * enlarge) {
        grid.last().add(0)
    }
}

(0 until enlarge).forEach { y ->
    (0 until enlarge).forEach { x ->
        original.forEachIndexed { gy, row ->
            row.forEachIndexed { gx, cell ->
                grid[y * original.size + gy][x * original[0].size + gx] = (cell + x + y).let { if (it > 9) it - 9 else it }
            }
        }
    }
}

val nextToFlood = mutableMapOf(grid[0][0] to mutableListOf(0 to 0)).withDefault { mutableListOf() }
val endY = grid.size - 1
val endX = grid[0].size - 1
var currentCost = 0
val bestCostOffer = mutableMapOf<Pair<Int, Int>, Int>()

while (true) {
    nextToFlood.getValue(currentCost).forEach { (y, x) ->
        if (y == endY && x == endX) {
            println(currentCost - original[0][0])
            exitProcess(0)
        }
        grid[y][x] = 0
        listOf(1 to 0, 0 to 1, -1 to 0, 0 to -1).map { (dx, dy) ->
            val neighborY = y + dy
            val neighborX = x + dx
            try {
                val nextCell = grid[neighborY][neighborX]
                bestCostOffer[neighborY to neighborX]?.let { offer ->
                    if (currentCost + nextCell >= offer) return@map
                } ?: run {
                    bestCostOffer[neighborY to neighborX] = currentCost + nextCell
                }

                if (nextCell != 0) {
                    nextToFlood[currentCost + nextCell] = nextToFlood.getValue(currentCost + nextCell).also { it.add(neighborY to neighborX) }
                }
            } catch (_: IndexOutOfBoundsException) { }
        }
    }
    nextToFlood.getValue(currentCost).clear()
    nextToFlood.remove(currentCost)
    currentCost++
}
