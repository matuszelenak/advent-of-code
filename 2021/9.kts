import java.io.File

val grid = File("9.in").readLines().map { l -> l.map { it.toString().toInt() } }

fun List<List<Int>>.lower(r: Int, c: Int, than: Int) = (getOrNull(r)?.getOrNull(c) ?: 10) > than

grid.mapIndexed { r, row ->
    row.filterIndexed { c, cell ->
        grid.lower(r - 1, c, cell) && grid.lower(r + 1, c, cell) && grid.lower(r, c - 1, cell) && grid.lower(r, c + 1, cell)
    }.let { it.count() + it.sum() }
}.sum()