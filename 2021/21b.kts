import java.math.BigInteger

val scores = mutableMapOf(0 to BigInteger.ZERO, 1 to BigInteger.ZERO)

(0 until 25).fold(listOf(Triple(0 to 5, 0 to 7, BigInteger.ONE))) { turnStates, turnId ->
    turnStates.filter { it.first.first < 21 }.flatMap { (opponentState, state, universes) ->
        val (score, position) = state
        listOf(3 to 1, 4 to 3, 5 to 6, 6 to 7, 7 to 6, 8 to 3, 9 to 1).map { (move, branching) ->
            val newPosition = (position + move).mod(10)
            val newScore = score + newPosition + 1
            Triple(newScore to newPosition, opponentState, universes * branching.toBigInteger())
        }
    }.groupBy { it.first to it.second }.map { group ->
        Triple(group.key.first, group.key.second, group.value.sumOf { it.third })
    }.also { newStates ->
        scores[turnId.mod(2)] = scores[turnId.mod(2)]!! + newStates.filter { it.first.first > 20 }.sumOf { it.third }
    }
}
scores.values.maxOrNull()