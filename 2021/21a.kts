import kotlin.system.exitProcess

fun generatePlayerTurns(startPos: Int, initialMove: Int) = sequence {
    var position = startPos
    var previousMove: Int? = null
    var score = 0

    while (true) {
        val currentMove = (previousMove?.let { it + 18 } ?: initialMove)
        position = (position + currentMove).mod(10)
        score += (position + 1)
        yield(position + 1 to score)
        previousMove = currentMove
    }
}

val p1 = generatePlayerTurns(7, 6).iterator()
val p2 = generatePlayerTurns(5, 15).iterator()

sequence {
    while (true) {
        yield(p1.next())
        yield(p2.next())
    }
}.zipWithNext().forEachIndexed { index, (curr, next) ->
    if (next.second >= 1000) {
        println(((index + 2) * 3) * curr.second)
        exitProcess(0)
    }
}