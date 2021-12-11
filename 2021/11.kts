import java.io.File

val octopuses = File("11.in").readLines().map { l -> l.map { it.toString().toInt() }.toMutableList() }

fun propagateEnergy(r: Int, c: Int): Int {
    var inspiredFlashes = 0
    (-1..1).map { rowDelta ->
        (-1..1).forEach { colDelta ->
            if (!(rowDelta == 0 && colDelta == 0)) {
                octopuses.getOrNull(r + rowDelta)?.getOrNull(c + colDelta) ?: return@forEach

                if (octopuses[r + rowDelta][c + colDelta] < 10) {
                    if (++octopuses[r + rowDelta][c + colDelta] == 10) {
                        inspiredFlashes += (1 + propagateEnergy(r + rowDelta, c + colDelta))
                    }
                }
            }
        }
    }
    return inspiredFlashes
}

var totalFlashes = 0
(1..1000000).first {
    octopuses.forEach { row -> row.forEachIndexed { index, _ -> row[index]++ } }

    val naturalFlashCoords = mutableListOf<Pair<Int, Int>>()
    octopuses.forEachIndexed { rowIndex, row ->
        row.forEachIndexed { colIndex, octopus ->
            if (octopus > 9) {
                naturalFlashCoords.add(rowIndex to colIndex)
            }
        }
    }
    naturalFlashCoords.forEach { (rowIndex, colIndex) ->
        totalFlashes += (1 + propagateEnergy(rowIndex, colIndex))
    }

    octopuses.forEachIndexed { rowIndex, row ->
        row.forEachIndexed { colIndex, octopus ->
            if (octopus > 9) {
                octopuses[rowIndex][colIndex] = 0
            }
        }
    }

    octopuses.all { row -> row.all { it == 0 } }
}
