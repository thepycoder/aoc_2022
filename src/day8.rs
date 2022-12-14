use std::fs;
use itertools::izip;
use ndarray::{Array, ArrayBase, OwnedRepr, Dim, Array2, Axis, s};
use ndarray_stats::QuantileExt;


pub fn day8_1(filepath: &str) -> Result<i32, std::io::Error> {
    let input_str: String = fs::read_to_string(filepath)?;
    let mut size: usize = 0;
    let trees: Vec<i32> = input_str
        .split("\n")
        .map(|treeline| {
            size = treeline.len();
            treeline
                .chars()
                .map(|tree| tree.to_digit(10).unwrap() as i32)
                .collect::<Vec<i32>>()
        })
        .flatten()
        .collect();

    let mut tree_array = Array2::from_shape_vec((size, size), trees).unwrap();
    let mut visibility: ArrayBase<OwnedRepr<i32>, Dim<[usize; 2]>> = Array::zeros((size, size));
    // dbg!(&tree_array.shape());
    // dbg!(&tree_array);

    for (mut row, mut visibility) in izip![tree_array.axis_iter_mut(Axis(0)), visibility.axis_iter_mut(Axis(0))]  {
        parse_visibility(&mut row, &mut visibility);
        parse_visibility(&mut row.slice_mut(s![..;-1]), &mut visibility.slice_mut(s![..;-1]));
    }

    for (mut col, mut visibility) in izip![tree_array.axis_iter_mut(Axis(1)), visibility.axis_iter_mut(Axis(1))]  {
        parse_visibility(&mut col, &mut visibility);
        parse_visibility(&mut col.slice_mut(s![..;-1]), &mut visibility.slice_mut(s![..;-1]));
    }

    // dbg!(&visibility);
    // dbg!(&visibility.sum());

    // dbg!(tree_array);


    Ok(visibility.sum())
}


pub fn day8_2(filepath: &str) -> Result<i32, std::io::Error> {
    let input_str: String = fs::read_to_string(filepath)?;
    let mut size: usize = 0;
    let trees: Vec<i32> = input_str
        .split("\n")
        .map(|treeline| {
            size = treeline.len();
            treeline
                .chars()
                .map(|tree| tree.to_digit(10).unwrap() as i32)
                .collect::<Vec<i32>>()
        })
        .flatten()
        .collect();

    let mut tree_array = Array2::from_shape_vec((size, size), trees).unwrap();
    let mut score: ArrayBase<OwnedRepr<i32>, Dim<[usize; 2]>> = Array::ones((size, size));
    // dbg!(&tree_array.shape());
    // dbg!(&tree_array);

    for (mut row, mut score) in izip![tree_array.axis_iter_mut(Axis(0)), score.axis_iter_mut(Axis(0))]  {
        parse_score(&mut row, &mut score);
        parse_score(&mut row.slice_mut(s![..;-1]), &mut score.slice_mut(s![..;-1]));
    }

    for (mut col, mut score) in izip![tree_array.axis_iter_mut(Axis(1)), score.axis_iter_mut(Axis(1))]  {
        parse_score(&mut col, &mut score);
        parse_score(&mut col.slice_mut(s![..;-1]), &mut score.slice_mut(s![..;-1]));
    }

    // dbg!(&score);
    // dbg!(&score.max());

    // dbg!(tree_array);


    Ok(*score.max().unwrap())
}

fn parse_visibility(row: &mut ArrayBase<ndarray::ViewRepr<&mut i32>, Dim<[usize; 1]>>, visibility: &mut ArrayBase<ndarray::ViewRepr<&mut i32>, Dim<[usize; 1]>>) -> () {
    let mut max = &mut -1i32;
    for (tree, visible) in izip![row, visibility] {
        if tree > max {
            max = tree;
            *visible = 1i32;
        }
    }
}

fn parse_score(row: &ArrayBase<ndarray::ViewRepr<&mut i32>, Dim<[usize; 1]>>, scores: &mut ArrayBase<ndarray::ViewRepr<&mut i32>, Dim<[usize; 1]>>) -> () {
    for (i, (tree, score)) in izip![row, scores].enumerate() {
        let mut cursor: usize;
        if i == 0 {
           cursor = i;
        } else {
            cursor = i-1;
        }
        while cursor > 0 && &row.slice(s![cursor]).into_scalar() < &tree {
            cursor -= 1;
        }
        *score *= (i - cursor) as i32;
    }
}



#[cfg(test)]
mod tests {
    // Note this useful idiom: importing names from outer (for mod tests) scope.
    use super::*;

    #[test]
    fn test_day8_1() {
        assert_eq!(day8_1("data/test8_1.txt").unwrap(), 21);
    }

    #[test]
    fn test_day8_2() {
        assert_eq!(day8_2("data/test8_1.txt").unwrap(), 8);
    }
}