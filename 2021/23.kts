import kotlin.math.pow

sealed class Node {
    abstract var neighbors: MutableList<Node>
}

abstract class HabitableNode(
    open var occupant: Int? = null
) : Node()

data class Street(
    val id: Int,
    override var occupant: Int? = null,
    override var neighbors: MutableList<Node> = mutableListOf()
) : HabitableNode(occupant) {
    override fun toString() = "Street $id"
}

data class Driveway(
    override var neighbors: MutableList<Node> = mutableListOf(),
    val owner: Int
) : Node() {
    override fun toString() = "Driveway for $owner"
}

data class Bunk(
    override var occupant: Int? = null,
    val owner: Int,
    var driveway: Driveway? = null,
    var previousField: Bunk? = null,
    var nextField: Bunk? = null
) : HabitableNode(
    occupant
) {
    override var neighbors: MutableList<Node> = mutableListOf()
        get() = listOfNotNull(driveway, previousField, nextField).toMutableList()

    override fun toString() = "Bunk of ${owner / 4} occupied by $occupant"
}

val inCategory = 4
val categories = 4

val sameCategory = { a: Int, b: Int -> a / inCategory == b / inCategory }

val initialConfig = mapOf(
    0 to listOf(12, 13, 14, 8),
    4 to listOf(15, 9, 4, 0),
    8 to listOf(5, 6, 1, 7),
    12 to listOf(2, 3, 10, 11)
)

val costs = (0 until categories * inCategory).associateWith { 10.0.pow(it / inCategory).toInt() }

val (dA, dB, dC, dD) = (0 until categories).map { Driveway(owner = it) }
val playerPositions: MutableList<HabitableNode> =
    listOf(dA, dB, dC, dD).zip(initialConfig.entries).flatMap { (driveway, config) ->
        val (owner, occupants) = config
        occupants.mapIndexed { bunkIndex, occupant ->
            val node = Bunk(
                owner = owner,
                occupant = occupant
            )
            if (bunkIndex == 0) {
                node.driveway = driveway
                driveway.neighbors.add(node)
            }
            node
        }.also { ownedBunks ->
            ownedBunks.zipWithNext().forEach { (first, second) ->
                first.nextField = second
                second.previousField = first
            }
        }.map { it.occupant to it }
    }.sortedBy { it.first }.map { it.second }.toMutableList()

val allBunks = playerPositions.toMutableList() as List<Bunk>

listOf(Street(0), Street(1), dA, Street(2), dB, Street(3), dC, Street(4), dD, Street(5), Street(6))
    .zipWithNext().forEach { (first, second) ->
        first.neighbors.add(second)
        second.neighbors.add(first)
    }

fun dfs(current: Node, from: Node?, dist: Int): Sequence<Pair<HabitableNode, Int>> = sequence {
    current.neighbors.forEach { neighbor ->
        if (neighbor != from) {
            if (neighbor is HabitableNode) {
                if (neighbor.occupant == null) {
                    yield(neighbor to dist)
                    yieldAll(dfs(neighbor, current, dist + 1))
                }
            } else yieldAll(dfs(neighbor, current, dist + 1))
        }
    }
}

fun iterateMovesV2(from: HabitableNode, playerId: Int, isLast: Boolean): Sequence<Pair<HabitableNode, Int>> {
    return dfs(from, null, 1).filter { (target, _) ->
        if (target is Bunk) {
            // Don't move to bunk that isn't yours
            if (!sameCategory(target.owner, playerId)) return@filter false

            // Don't move within your own bunks
            if (from is Bunk) return@filter false

            if (target.nextField != null) {
                var curr: Bunk = target
                while (curr.nextField != null) {
                    curr = curr.nextField!!
                    // You must move to the bottom, can't stay in middle
                    if (curr.occupant == null) return@filter false
                    // If this bunk contains some impostor, can't move there
                    if (!sameCategory(curr.occupant!!, target.owner)) return@filter false
                }
            }
            // You can move to the bottom of your bunk
            true
        } else true
    }.let {
        if (isLast) {
            it.filter { (target, _) -> target is Bunk && sameCategory(target.owner, playerId) }
        } else it
    }.map { (target, dist) ->
        target to dist * costs[playerId]!!
    }
}

var bestScore = Int.MAX_VALUE

fun iterateSolutions(
    positions: MutableList<HabitableNode>,
    movesLeft: MutableList<Int>,
    movesSoFar: List<Pair<Int, HabitableNode>>,
    costSoFar: Int
) {
    if (allBunks.all { bunk -> bunk.occupant?.let { sameCategory(it, bunk.owner) } == true }) {
        bestScore = minOf(bestScore, costSoFar)
        println(bestScore)
    }

    movesLeft.forEachIndexed { playerId, moveCount ->
        if (moveCount > 0) {
            if (allBunks.filter { sameCategory(playerId, it.owner) }
                    .all { bunk -> bunk.occupant?.let { sameCategory(it, bunk.owner) } == true }) {
                return@forEachIndexed
            }

            val possibleMoves = iterateMovesV2(positions[playerId], playerId, moveCount == 1)
            possibleMoves.filter { costSoFar + it.second < bestScore }.forEach { (targetNode, moveCost) ->
                val oldPosition = positions[playerId]
                oldPosition.occupant = null
                positions[playerId] = targetNode
                targetNode.occupant = playerId
                movesLeft[playerId]--

                iterateSolutions(
                    positions,
                    movesLeft,
                    movesSoFar + (playerId to targetNode),
                    costSoFar + moveCost
                )

                targetNode.occupant = null
                oldPosition.occupant = playerId
                positions[playerId] = oldPosition
                movesLeft[playerId]++
            }
        }
    }
}

iterateSolutions(playerPositions, MutableList(categories * inCategory) { 2 }, emptyList(), 0)
