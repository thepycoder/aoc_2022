use std::pin::Pin;
use std::{fs, thread::current};
use slab_tree::iter::LevelOrder;
use trees::Node;
use trees::tr;
use trees::Tree;
use slab_tree::*;

#[derive(Debug)]
struct Folder {
    name: String,
    size: u64
}

fn add_size(node: &mut NodeMut<Folder>, size: u64) {
    if node.parent().is_none() {
        // We've reached the top, nothing more to do here
        return
    }
    let mut folder = node.data();
    folder.size += size;

    let mut parent = node.parent().unwrap();

    add_size(&mut parent, size);
}


pub fn day7_1(filepath: &str) -> Result<u64, std::io::Error> {
    let commands: String = fs::read_to_string(filepath)?.parse().unwrap();
    let mut tree = TreeBuilder::new().with_root(Folder{name: "root".to_string(), size: 0}).build();
    let mut current_node_id = tree.root_id().unwrap();
    let result = commands
        .split("$ ")
        .skip(1)
        .map(|single_command| match single_command.chars().next().unwrap() {
           'c' => {
                let folder_to_go = single_command.split(" ").collect::<Vec<&str>>()[1];
                match folder_to_go {
                    "..\n" => {
                        let current_node = tree.get(current_node_id).unwrap();
                        let parent = current_node.parent().unwrap();
                        current_node_id = parent.node_id();
                    },
                    _ => {
                        let new_subfolder = Folder{name: folder_to_go.replace("\n", "").to_string(), size: 0};
                        let mut current_node = tree.get_mut(current_node_id).unwrap();
                        let new_node = current_node.append(new_subfolder);
                        current_node_id = new_node.node_id();
                    }
                }
           },
           'l' => {
                let dir_or_number: () = single_command.lines().map(|ls_output_line| {
                    let ls_output_dir_or_number = ls_output_line.split(" ").collect::<Vec<_>>()[0];
                    // dbg!(ls_output_dir_or_number);
                    match ls_output_dir_or_number {
                        "dir" => (),
                        "ls" => (),
                        _ => {
                            let size = ls_output_dir_or_number.parse::<u64>().unwrap();
                            let mut current_node = tree.get_mut(current_node_id).unwrap();
                            add_size(&mut current_node, size);
                        }
                    }
                }).collect();
           },
           _ => ()
        })
        .collect::<Vec<_>>();
    
    // dbg!(commands.split("$ ").collect::<Vec<_>>());
    // dbg!(tree);
    let result: u64 = tree.root()
        .unwrap()
        .traverse_pre_order()
        .map(|node_ref| {
            let folder = node_ref.data();
            dbg!(&folder.name);
            dbg!(folder.size);
            if folder.size <= 100000 {
                folder.size
            } else {
                0
            }
        })
        .map(|item| dbg!(item))
        .sum();
        // .collect::<Vec<u64>>();

    Ok(result)
}


pub fn day7_2(filepath: &str) -> Result<u64, std::io::Error> {
    let commands: String = fs::read_to_string(filepath)?.parse().unwrap();
    let mut tree = TreeBuilder::new().with_root(Folder{name: "root".to_string(), size: 0}).build();
    let mut current_node_id = tree.root_id().unwrap();
    let result = commands
        .split("$ ")
        .skip(1)
        .map(|single_command| match single_command.chars().next().unwrap() {
           'c' => {
                let folder_to_go = single_command.split(" ").collect::<Vec<&str>>()[1];
                match folder_to_go {
                    "..\n" => {
                        let current_node = tree.get(current_node_id).unwrap();
                        let parent = current_node.parent().unwrap();
                        current_node_id = parent.node_id();
                    },
                    _ => {
                        let new_subfolder = Folder{name: folder_to_go.replace("\n", "").to_string(), size: 0};
                        let mut current_node = tree.get_mut(current_node_id).unwrap();
                        let new_node = current_node.append(new_subfolder);
                        current_node_id = new_node.node_id();
                    }
                }
           },
           'l' => {
                let dir_or_number: () = single_command.lines().map(|ls_output_line| {
                    let ls_output_dir_or_number = ls_output_line.split(" ").collect::<Vec<_>>()[0];
                    // dbg!(ls_output_dir_or_number);
                    match ls_output_dir_or_number {
                        "dir" => (),
                        "ls" => (),
                        _ => {
                            let size = ls_output_dir_or_number.parse::<u64>().unwrap();
                            let mut current_node = tree.get_mut(current_node_id).unwrap();
                            add_size(&mut current_node, size);
                        }
                    }
                }).collect();
           },
           _ => ()
        })
        .collect::<Vec<_>>();
    
    // dbg!(commands.split("$ ").collect::<Vec<_>>());
    // dbg!(tree);
    let result: Vec<u64> = tree.root()
        .unwrap()
        .traverse_pre_order()
        .map(|node_ref| {
            let folder = node_ref.data();
            folder.size
            // dbg!(&folder.name);
            // dbg!(folder.size);
            // if folder.size >= 8381165 {
            //     folder.size
            // } else {
            //     folder.size
            // }
        })
        // .map(|item| dbg!(item))
        .collect::<Vec<u64>>();
    
    let total_used_size = result.iter().max().unwrap();
    let total_free_size = 70000000 - total_used_size;
    let minimum_needed_free_size = 30000000 - total_free_size;
    dbg!(minimum_needed_free_size);

    let answer = result.iter().filter(|value| value >= &&minimum_needed_free_size).min();
    dbg!(answer);
        // .min()
        // .unwrap();

    Ok(*answer.unwrap())
}


#[cfg(test)]
mod tests {
    // Note this useful idiom: importing names from outer (for mod tests) scope.
    use super::*;

    #[test]
    fn test_day6_1() {
        assert_eq!(day7_1("data/test7_1.txt").unwrap(), 95437);
    }

    #[test]
    fn test_day6_2() {
        assert_eq!(day7_2("data/test7_1.txt").unwrap(), 24933642);
    }
}