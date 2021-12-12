import java.io.File

val edges = mutableMapOf<String, MutableList<String>>().withDefault { mutableListOf() }
File("12.in").readLines().forEach { line ->
    val (nodeA, nodeB) = line.split("-")
    edges[nodeA] = edges.getValue(nodeA).also { it.add(nodeB) }
    edges[nodeB] = edges.getValue(nodeB).also { it.add(nodeA) }
}

val String.isSmall: Boolean
    get() = lowercase() == this

fun iteratePaths(currentNode: String, alreadyVisitedSmall: Set<String>, path: List<String>): Sequence<List<String>> {
    if (currentNode == "end") return sequenceOf(path)

    return sequence {
        edges.getValue(currentNode).forEach { targetNode ->
            if (targetNode.isSmall) {
                if (!alreadyVisitedSmall.contains(targetNode)) {
                    yieldAll(
                        iteratePaths(
                            targetNode,
                            alreadyVisitedSmall + setOf(targetNode),
                            path + listOf(targetNode)
                        )
                    )
                }
            } else {
                if (!path.contains(targetNode) || path.drop(path.lastIndexOf(targetNode)).any { it.isSmall }) {
                    yieldAll(
                        iteratePaths(
                            targetNode,
                            alreadyVisitedSmall,
                            path + listOf(targetNode)
                        )
                    )
                }
            }
        }
    }
}

iteratePaths("start", setOf("start"), listOf("start")).map { it.joinToString(",") }.toList().size