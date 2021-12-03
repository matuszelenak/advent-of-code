data class Node(
        val nodes: MutableMap<Char, Node> = mutableMapOf<Char, Node>().withDefault { Node() },
        val counts: MutableMap<Char, Int> = mutableMapOf<Char, Int>().withDefault { 0 }
)

val startNode = Node()

java.io.File("3a.in").readLines().forEach { line ->
    var currentNode = startNode
    line.forEach { c ->
        currentNode.counts[c] = currentNode.counts.getValue(c) + 1
        currentNode.nodes[c] = currentNode.nodes.getValue(c)
        currentNode = currentNode.nodes[c]!!
    }
}

val oxy = sequence {
    var currentNode = startNode
    while (true) {
        currentNode.counts.toSortedMap(compareBy { -it.code }).maxByOrNull { it.value }?.key?.also {
            yield(it)
            currentNode = currentNode.nodes[it]!!
        } ?: break
    }
}.joinToString("").toInt(2)

val scrubber = sequence {
    var currentNode = startNode
    while (true) {
        currentNode.counts.toSortedMap(compareBy { it.code }).minByOrNull { it.value }?.key?.also {
            yield(it)
            currentNode = currentNode.nodes[it]!!
        } ?: break
    }
}.joinToString("").toInt(2)

oxy * scrubber