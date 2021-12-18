import java.io.File
import kotlin.math.ceil
import kotlin.math.floor

data class Node(
    var number: Int? = null,
    var right: Node? = null,
    var left: Node? = null,
    var parent: Node? = null
) {
    override fun toString(): String {
        return number?.toString() ?: "[$left,$right]"
    }

    val magnitude: Int
        get() = number ?: (3 * left!!.magnitude + 2 * right!!.magnitude)

    operator fun plus(other: Node) = Node().also { newRoot ->
        newRoot.left = this.also { it.parent = newRoot }
        newRoot.right = other.also { it.parent = newRoot }
    }

    fun explode(): Boolean {
        this.findNearestLeft()?.also { it.number = it.number!! + this.left!!.number!! }
        this.findNearestRight()?.also { it.number = it.number!! + this.right!!.number!! }

        if (this === this.parent!!.left) {
            this.parent!!.left = Node(number = 0, parent = this.parent)
        } else {
            this.parent!!.right = Node(number = 0, parent = this.parent)
        }
        return true
    }

    fun split(): Boolean {
        val newNode = Node(parent = this.parent)
        val left = Node(parent = newNode, number = floor(this.number!!.toDouble() / 2).toInt())
        val right = Node(parent = newNode, number = ceil(this.number!!.toDouble() / 2).toInt())
        newNode.left = left
        newNode.right = right
        if (this === this.parent!!.left) {
            this.parent!!.left = newNode
        } else {
            this.parent!!.right = newNode
        }
        return true
    }

    private fun findNearestLeft(): Node? {
        // first climb up until you find an ancestor that has a left child
        var curr: Node? = this
        while (curr != null) {
            if (curr === curr.parent?.right) {
                curr = curr.parent
                break
            }
            curr = curr.parent
        }

        if (curr == null) return null
        curr = curr.left
        while (curr?.right != null) {
            curr = curr.right
        }
        return curr
    }

    private fun findNearestRight(): Node? {
        var currr: Node? = this
        while (currr != null) {
            if (currr === currr.parent?.left) {
                currr = currr.parent
                break
            }
            currr = currr.parent
        }

        if (currr == null) return null

        currr = currr.right
        while (currr?.left != null) {
            currr = currr.left
        }
        return currr
    }

    private fun findCombustible(depth: Int = 0): Node? {
        if (depth >= 4 && number == null) return this
        return this.left?.findCombustible(depth + 1) ?: this.right?.findCombustible(depth + 1)
    }

    private fun findToSplit(): Node? {
        return if (number != null) {
            if (number!! > 9) this else null
        } else {
            left?.findToSplit() ?: right?.findToSplit()
        }
    }

    fun reduced(): Node {
        while ((findCombustible()?.explode() ?: findToSplit()?.split()) == true) {
        }
        return this
    }
}

fun Iterator<Char>.parseNodeTree(parent: Node? = null): Node {
    val c = this.next()
    return if ("01234567890".contains(c)) {
        Node(
            number = c.toString().toInt(),
            parent = parent
        )
    } else {
        Node().also {
            it.parent = parent
            it.left = parseNodeTree(it)
            this.next()
            it.right = parseNodeTree(it)
            this.next()
        }
    }
}

File("18.in").readLines().map { it.iterator().parseNodeTree() }.reduce { acc, number ->
    (acc + number).reduced()
}.magnitude

(0 until 100).flatMap { i ->
    (0 until 100).mapNotNull { j ->
        if (i == j) null else {
            val (a, b) = File("18.in").readLines().map { it.iterator().parseNodeTree() }.slice(listOf(i, j))
            (a + b).reduced().magnitude
        }
    }
}.maxOrNull()