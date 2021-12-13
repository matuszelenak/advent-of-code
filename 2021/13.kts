import java.io.File

fun <T> Iterable<T>.splitOn(cond: (T) -> Boolean): List<List<T>> {
    return sequence {
        val acc = mutableListOf<T>()
        this@splitOn.forEach { elem ->
            if (cond.invoke(elem)) {
                yield(acc.toList())
                acc.clear()
            } else acc.add(elem)
        }
        if (acc.isNotEmpty()) yield(acc)
    }.toList()
}

fun Pair<Int, Int>.fold(pivotX: Int?, pivotY: Int?): Pair<Int, Int> {
    return (if (pivotX != null) {
        if (first < pivotX) this else (2 * pivotX - first) to second
    } else if (pivotY != null) {
        if (second < pivotY) this else first to (2 * pivotY - second)
    } else throw IllegalArgumentException())
}

fun debug(d: Iterable<Pair<Int, Int>>) {
    (0..d.maxOf { it.second }).forEach { y ->
        (0..d.maxOf { it.first }).forEach { x ->
            if (d.contains(x to y)) print('#') else print('.')
        }
        println()
    }
    println()
}

val (dots, instructions) = File("13.in").readLines().splitOn { it.isBlank() }.let {
    it[0].map { line ->
        val (x, y) = line.split(",").map(String::toInt)
        x to y
    }.toSet() to it[1].map { line ->
        val (axis, coordinate) = line.split("=")
        if (axis.endsWith('x')) {
            coordinate.toInt() to null
        } else {
            null to coordinate.toInt()
        }
    }
}

instructions.fold(dots) { acc, instruction ->
    acc.map { it.fold(instruction.first, instruction.second) }.toSet()
}.let {
    debug(it)
    it.size
}