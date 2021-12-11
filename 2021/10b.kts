import java.io.File

val pairs = mapOf(
        ')' to '(',
        ']' to '[',
        '}' to '{',
        '>' to '<'
)
val scores = mapOf('(' to 1L, '[' to 2L, '{' to 3L, '<' to 4L)

File("10.in").readLines().mapNotNull { line ->
    val stack = mutableListOf<Char>()
    for (c in line) {
        if (pairs.containsKey(c)) {
            try {
                stack.removeLast().let {
                    if (it != pairs[c]) throw NoSuchElementException()
                }
            } catch (e: NoSuchElementException) {
                return@mapNotNull null
            }
        } else stack.add(c)
    }
    stack.reversed().fold(0L) { acc, c -> acc * 5L + scores[c]!! }
}.sorted().let { it[it.size / 2] }