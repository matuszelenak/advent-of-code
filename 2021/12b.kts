import java.io.File

val edges = mutableMapOf<String, MutableList<String>>().withDefault { mutableListOf() }
File("12.in").readLines().forEach { line ->
    val (nodeA, nodeB) = line.split("-")
    edges[nodeA] = edges.getValue(nodeA).also { it.add(nodeB) }
    edges[nodeB] = edges.getValue(nodeB).also { it.add(nodeA) }
}

val String.isSmall: Boolean
    get() = lowercase() == this

fun iteratePaths(currentNode: String, alreadyVisitedSmall: Set<String>, path: List<String>, exception: String?): Sequence<List<String>> {
    if (currentNode == "end") return sequenceOf(path)

    return sequence {
        edges.getValue(currentNode).forEach { targetNode ->
            if (targetNode.isSmall) {
                if (!alreadyVisitedSmall.contains(targetNode)) {
                    yieldAll(
                        iteratePaths(
                            targetNode,
                            alreadyVisitedSmall + if (targetNode == exception) emptySet() else setOf(targetNode),
                            path + listOf(targetNode),
                            if (targetNode == exception) null else exception
                        )
                    )
                }
            } else {
                if (!path.contains(targetNode) || path.drop(path.lastIndexOf(targetNode)).any { it.isSmall }) {
                    yieldAll(
                        iteratePaths(
                            targetNode,
                            alreadyVisitedSmall,
                            path + listOf(targetNode),
                            exception
                        )
                    )
                }
            }
        }
    }
}

edges.keys.filter { it.isSmall && !listOf("start", "end").contains(it) }.flatMap { smol ->
    iteratePaths("start", setOf("start"), listOf("start"), smol).map { it.joinToString(",") }.toList()
}.toSet().size
