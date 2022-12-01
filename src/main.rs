use std::io;

mod day1;
mod day2;

fn main() -> io::Result<()> {
    let total = day1::day1_1("data/input1_1.txt");
    println!("{}", total.unwrap());

    let total_2 = day1::day1_2("data/input1_1.txt");
    println!("{}", total_2.unwrap());
    Ok(())
}
