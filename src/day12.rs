use ndarray::{Array2, Axis, Ix2};
use std::collections::VecDeque;
use std::fs;
use std::str;
use std::io::prelude::*;
use std::io::BufReader;
use std::collections::HashMap;

#[derive(Debug, Clone, Copy, PartialEq, Hash, Eq)]
struct Coord {
    x: usize,
    y: usize,
    value: u8
}

fn get_neighbors(array: &Array2<u8>, coord: &Coord) -> Vec<Coord> {
    let mut neighbors = Vec::new();

    // Check for elements above and below the given coord
    if coord.x > 0 && coord.x < array.len_of(Axis(0)) {
        neighbors.push(Coord{ x: coord.x - 1, y: coord.y, value: array[[coord.x - 1, coord.y]] });
    }
    if coord.x < array.len_of(Axis(0)) - 1 {
        neighbors.push(Coord{ x: coord.x + 1, y: coord.y, value: array[[coord.x + 1, coord.y]]});
    }

    // Check for elements to the left and right of the given coord
    if coord.y > 0 && coord.y < array.len_of(Axis(1)) {
        neighbors.push(Coord{ x: coord.x, y: coord.y - 1, value: array[[coord.x, coord.y - 1]]});
    }
    if coord.y < array.len_of(Axis(1)) - 1 {
        neighbors.push(Coord{ x: coord.x, y: coord.y + 1, value: array[[coord.x, coord.y + 1]]});
    }

    neighbors
}

fn read_grid(filepath: &str) -> (Array2<u8>, Coord, Coord) {
    let file = fs::File::open(filepath).expect("Failed to open file");
    let reader = BufReader::new(file);

    let mut starting_position: Coord = Coord { x: 0, y: 0, value: 0 };
    let mut ending_position: Coord = Coord { x: 0, y: 0, value: 0 };

    let mut grid: Vec<Vec<u8>> = Vec::new();

    for (i, line) in reader.lines().enumerate() {
        let line = line.expect("Failed to read line");
        let mut chars: Vec<u8> = line.chars().map(|c| c as u8).collect();

        let starting_col_option = chars.iter().position(|&c| c == 83u8);
        if !starting_col_option.is_none() {
            starting_position = Coord {x: i, y: starting_col_option.unwrap(), value: 'a' as u8};
            chars[starting_col_option.unwrap()] = 'a' as u8;
        }

        let ending_col_option = chars.iter().position(|&c| c == 69u8);
        if !ending_col_option.is_none() {
            ending_position = Coord {x: i, y: ending_col_option.unwrap(), value: 'z' as u8};
            chars[ending_col_option.unwrap()] = 'z' as u8;
        }
        grid.push(chars);
    }

    let rows = grid.len();
    let cols = grid[0].len();

    let shape = (rows, cols);
    let data = grid.into_iter().flatten().collect::<Vec<u8>>();

    (Array2::from_shape_vec(shape, data).expect("Failed to create 2D array"), starting_position, ending_position)
}

pub fn day12_1(filepath: &str) -> Result<usize, std::io::Error> {

    let (grid, starting_position, ending_position) = read_grid(filepath);
    dbg!(&grid);
    dbg!(starting_position);
    dbg!(ending_position);

    let result = solve(starting_position, &grid, ending_position);
    result
}

pub fn day12_2(filepath: &str) -> Option<usize> {

    let (grid, starting_position, ending_position) = read_grid(filepath);

    let mut starting_positions: Vec<Coord> = Vec::new();
    for ((i, j), val) in grid.indexed_iter() {
        if val == &('a' as u8) {
            starting_positions.push(Coord { x: i, y: j, value: *val })
        }
    }

    let mut results: Vec<usize> = Vec::new();
    for starting_position in starting_positions {
        let result = solve(starting_position, &grid, ending_position).unwrap();
        results.push(result);
    }

    // dbg!(&results);
    results.sort_unstable();
    return results.first().copied();

}

fn solve(starting_position: Coord, grid: &ndarray::ArrayBase<ndarray::OwnedRepr<u8>, ndarray::Dim<[usize; 2]>>, ending_position: Coord) -> Result<usize, std::io::Error> {
    // While pop from queue
    let mut frontier: VecDeque<Coord> = VecDeque::new();
    let mut came_from: HashMap<Coord, Coord> = HashMap::new();
    frontier.push_back(starting_position);
    came_from.insert(starting_position, Coord { x: 0, y: 0, value: 0 });
    while let Some(current_coord) = frontier.pop_front() {
        // dbg!(path.len());
        // dbg!(deque.len());

        // Get neighbors (both Coord and Value)
        let neighbors = get_neighbors(&grid, &current_coord);

        // For each neighbor
        for neighbor in neighbors {
            // Check if value <= Current Coord value + 1
            if neighbor.value <= current_coord.value + 1 && !came_from.contains_key(&neighbor) {
                // Check if Coord is not Coord(E)
                if neighbor == ending_position {
                    came_from.insert(neighbor, current_coord);
                    break;
                }

                frontier.push_back(neighbor);
                came_from.insert(neighbor, current_coord);
            }
        }
    }
    let mut path: Vec<&Coord> = Vec::new();
    let mut current = &ending_position;
    while current != &starting_position {
        path.push(current);
        let cf = came_from.get(&current);
        if cf.is_none() {
            return Ok(999);
        }
        current = cf.unwrap();
    }
    Ok(path.len())
}


#[cfg(test)]
mod tests {
    // Note this useful idiom: importing names from outer (for mod tests) scope.
    use super::*;

    #[test]
    fn test_day12_1() {
        assert_eq!(day12_1("data/test12_1.txt").unwrap(), 31);
    }

    #[test]
    fn test_day12_2() {
        assert_eq!(day12_2("data/test12_1.txt").unwrap(), 29);
    }
}