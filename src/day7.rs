use std::pin::Pin;
use std::{fs, thread::current};
use trees::Node;
use trees::tr;
use trees::Tree;
use slab_tree::*;

struct Folder {
    name: String,
    size: u64
}

fn add_size(folder: &Node<Folder>, size: u64) {
    if folder.parent().is_none() {
        // We've reached the top, nothing more to do here
        return
    }
     let folder_data = *folder.data_mut();
     folder_data.size += size;
    add_size(folder.parent().unwrap(), size);
}


pub fn day7_1(filepath: &str) -> Result<usize, std::io::Error> {
    let commands: String = fs::read_to_string(filepath)?.parse().unwrap();
    let mut tree: Tree<Folder> = Tree::new(Folder{name: "root".to_string(), size: 0});
    let mut current_node = tree.root_mut();
    let result = commands
        .split("$ ")
        .skip(1)
        .map(|single_command| match single_command.chars().next().unwrap() {
           'c' => {
                let folder_to_go = single_command.split(" ").collect::<Vec<&str>>()[1];
                match folder_to_go {
                    ".." => {
                        let parent = current_node.parent();
                        current_node = parent.unwrap();
                    },
                    _ => {
                        let new_subfolder = Folder{name: folder_to_go.to_string(), size: 0};
                        let new_subtree = Tree::new(new_subfolder);
                        let new_node = new_subtree.root_mut();
                        current_node = new_node;
                        current_node.push_back(new_subtree);
                    }
                }
           },
           'l' => {
                let dir_or_number = single_command.lines().map(|ls_output_line| {
                    let ls_output_dir_or_number = ls_output_line.split(" ").collect::<Vec<_>>()[0];
                    match ls_output_dir_or_number {
                        "dir" => (),
                        _ => {
                            let size = ls_output_dir_or_number.parse::<u64>().unwrap();
                            add_size(current_node, size);
                        }
                    }
                });
           },
           _ => ()
        })
        .collect::<Vec<_>>();
    dbg!(commands.split("$ ").collect::<Vec<_>>());

    Ok(0)
}


#[cfg(test)]
mod tests {
    // Note this useful idiom: importing names from outer (for mod tests) scope.
    use super::*;

    #[test]
    fn test_day6_1() {
        assert_eq!(day7_1("data/test7_1.txt").unwrap(), 7);
    }

//     #[test]
//     fn test_day6_2() {
//         assert_eq!(day7_1("data/test6_2.txt", 4).unwrap(), 5);
//     }
}