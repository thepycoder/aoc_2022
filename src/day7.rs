use std::fs;
use slab_tree::*;

#[derive(Debug)]
struct Folder {
    _name: String,
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

fn update_tree(commands: String, tree: &mut slab_tree::Tree<Folder>) {
    let mut current_node_id = tree.root_id().unwrap();  // track on which node in the tree we are right now
    let _result = commands
        .split("$ ")  // First split off each command and its associated output if any
        .skip(1) // Skipt the first line because it will be empty (rust things)
        .map(|single_command| match single_command.chars().next().unwrap() {  // For every command, check the first character to see which command it is
           'c' => {
                let folder_to_go = single_command.split(" ").collect::<Vec<&str>>()[1];  // If it's cd, get the folder we need to go to
                match folder_to_go {
                    "..\n" => {  // if that folder is .., simply update our current node tracker
                        let current_node = tree.get(current_node_id).unwrap();
                        let parent = current_node.parent().unwrap();
                        current_node_id = parent.node_id();
                    },
                    _ => {  // If it is anything else, we need to create that new folder and add it to our tree
                        let new_subfolder = Folder{_name: folder_to_go.replace("\n", "").to_string(), size: 0};
                        let mut current_node = tree.get_mut(current_node_id).unwrap();
                        let new_node = current_node.append(new_subfolder);
                        // When this new folder is created, go into it by setting the current node tracker as such
                        current_node_id = new_node.node_id();
                    }
                }
           },
           'l' => {  // if it's ls, we want to process its output
                let _dir_or_number: () = single_command.lines().map(|ls_output_line| {  // for every line of ls output
                    let ls_output_dir_or_number = ls_output_line.split(" ").collect::<Vec<_>>()[0];  // get the first thing on the line
                    // dbg!(ls_output_dir_or_number);
                    match ls_output_dir_or_number {
                        "dir" => (),  // if its dir, it means a folder that has no size, so we don't care
                        "ls" => (), // if it's the command itself, we don't care
                        _ => {  // if it's a file we want to attach the filesize to this node and every parent (parent folder)
                            let size = ls_output_dir_or_number.parse::<u64>().unwrap();
                            let mut current_node = tree.get_mut(current_node_id).unwrap();
                            // add_size will recursively update all parents in the tree
                            add_size(&mut current_node, size);
                        }
                    }
                }).collect();
           },
           _ => ()
        })
        .collect::<Vec<_>>();
}


pub fn day7_1(filepath: &str) -> Result<u64, std::io::Error> {
    let commands: String = fs::read_to_string(filepath)?.parse().unwrap();
    let mut tree = TreeBuilder::new().with_root(Folder{_name: "root".to_string(), size: 0}).build();
    update_tree(commands, &mut tree);
    
    let result: u64 = tree.root()
        .unwrap()
        .traverse_pre_order()
        .map(|node_ref| {
            let folder = node_ref.data();
            if folder.size <= 100000 {
                folder.size
            } else {
                0
            }
        })
        // .map(|item| dbg!(item))
        .sum();

    Ok(result)
}


pub fn day7_2(filepath: &str) -> Result<u64, std::io::Error> {
    let commands: String = fs::read_to_string(filepath)?.parse().unwrap();
    let mut tree = TreeBuilder::new().with_root(Folder{_name: "root".to_string(), size: 0}).build();
    update_tree(commands, &mut tree);
    
    let result: Vec<u64> = tree.root()
        .unwrap()
        .traverse_pre_order()
        .map(|node_ref| {
            let folder = node_ref.data();
            folder.size

        })
        .collect::<Vec<u64>>();
    
    let total_used_size = result.iter().max().unwrap();
    let total_free_size = 70000000 - total_used_size;
    let minimum_needed_free_size = 30000000 - total_free_size;

    let answer = result.iter().filter(|value| value >= &&minimum_needed_free_size).min();

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