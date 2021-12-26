import java.io.File

var grid = File("25.in").readLines().map { line -> line.map { it } }
val dy = grid.size
val dx = grid[0].size

var movementDetected = false
var steps = 0
do {
    movementDetected = false
    val afterEast = grid.map { row -> row.map { it }.toMutableList() }

    grid.forEachIndexed { y, row ->
        row.forEachIndexed { x, c ->
            if (c == '>') {
                val (nY, nX) = y to (x + 1).mod(dx)
                if (grid[nY][nX] == '.') {
                    movementDetected = true
                    afterEast[nY][nX] = '>'
                    afterEast[y][x] = '.'
                }
            }
        }
    }

    val afterSouth = afterEast.map { row -> row.map { it }.toMutableList() }

    afterEast.forEachIndexed { y, row ->
        row.forEachIndexed { x, c ->
            if (c == 'v') {
                val (nY, nX) = (y + 1).mod(dy) to x
                if (afterEast[nY][nX] == '.') {
                    movementDetected = true
                    afterSouth[nY][nX] = 'v'
                    afterSouth[y][x] = '.'
                }
            }
        }
    }

    grid = afterSouth
    steps++
} while (movementDetected)

println(steps)