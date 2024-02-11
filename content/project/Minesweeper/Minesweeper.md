---
title: 扫雷游戏Minesweeper
date: '2024-02-11'
summary: 大一下学期《程序设计语言》的最后一次作业，虽然难度不高、老师也给出了一定的代码框架，但于我而言却是独一无二的存在。
tags:
  - 课程设计
share: false
---



## 头文件内容

```c++
#ifndef FP_H_
#define FP_H_

const int MAX_ROWS = 25;
const int MAX_COLS = 25;
const int MAX_CELLS = MAX_ROWS * MAX_COLS;

enum Cell {
	HIDDEN = -4,
	FLAGGED = -3,
	SAFE = -2,
	MINE = -1,
	ZERO = 0,
	ONE = 1,
	TWO = 2,
	THREE = 3,
	FOUR = 4,
	FIVE = 5,
	SIX = 6,
	SEVEN = 7,
	EIGHT = 8
};

class Mine_Sweeper{
private:
    Cell grid[MAX_ROWS][MAX_COLS];
    bool has_mine[MAX_ROWS][MAX_COLS]={0};
    int game_stats[4]={0};// num_rows, num_cols, num_flags_left, num_incorrect_flags.
    bool mine_exploded=false;
public:
    Mine_Sweeper(){} 
    Mine_Sweeper(int rows,int cols); 
    int get_num_rows(){return game_stats[0];}
    int get_num_cols(){return game_stats[1];}
    int get_num_flags_left(){return game_stats[2];}
    bool is_revealed(int row,int col){return grid[row][col]>=0;}
    bool is_flagged(int row,int col){return grid[row][col]==FLAGGED;}
    bool is_mine_exploded(){return mine_exploded;}
    bool is_succeeded(){return mine_exploded==false && game_stats[2]==0 && game_stats[3]==0 ;}

    void display_grid();
    void display_answer();
    void reveal(int row, int col);
    void flag(int row, int col);

    friend void generate_grid(Mine_Sweeper& my_mine_sweeper);
};

#endif /* FP_H_ */
```

## 源文件内容

```c++
#include <iostream>
#include <stdlib.h>
#include <time.h>
using namespace std;

#include "mine_sweeper.h"
int SEED = time(0);

// Implement the display() and display_answer() functions of Class
void Mine_Sweeper::display_grid()
{
	char print[MAX_ROWS][MAX_COLS];
	for (int i = 0; i < game_stats[0]; i++) {
		for (int j = 0; j < game_stats[1]; j++) {
			switch (grid[i][j]) {
			case ONE:
				print[i][j] = '1';
				break;
			case TWO:
				print[i][j] = '2';
				break;
			case THREE:
				print[i][j] = '3';
				break;
			case FOUR:
				print[i][j] = '4';
				break;
			case FIVE:
				print[i][j] = '5';
				break;
			case SIX:
				print[i][j] = '6';
				break;
			case SEVEN:
				print[i][j] = '7';
				break;
			case EIGHT:
				print[i][j] = '8';
				break;
			case HIDDEN:
				print[i][j] = 'o';
				break;
			case FLAGGED:
				print[i][j] = 'x';
				break;
			case SAFE:
				print[i][j] = '?';
				break;
			case MINE:
				print[i][j] = '!';
				break;
			case ZERO:
				print[i][j] = '.';
				break;
			}
		}
	}
	cout << endl;
	cout << "   ";
	for (int i = 0; i < game_stats[1]; i++)
		cout << static_cast<char>('A' + i) << " ";
	cout << endl;
	for (int i = 0; i < game_stats[0]; i++) {
		if (i < 9)
			cout << " " << i + 1 << " ";
		else
			cout << i + 1 << " ";
		for (int j = 0; j < game_stats[1]; j++) {
			cout << print[i][j] << " ";
			if (j == game_stats[1] - 1)
				cout << endl;
		}
	}
	cout << endl;
	cout << "Flags Left: " << game_stats[2] << endl;
	cout << endl;
}

void Mine_Sweeper::display_answer()
{
	//在先前基础上把错误标记的雷以及未标记的雷显示出来
	for (int i = 0; i < game_stats[0]; i++) {
		for (int j = 0; j < game_stats[1]; j++) {
			if (has_mine[i][j] == false && grid[i][j] == FLAGGED)
				grid[i][j] = SAFE;
			if (has_mine[i][j] == true && grid[i][j] == HIDDEN)
				grid[i][j] = MINE;
		}
	}
	display_grid();
}

// Implement the reveal() function of Class
void Mine_Sweeper::reveal(int row, int col)
{
	if (is_revealed(row, col) == true)
		return;
	if (has_mine[row][col] == true) {
		grid[row][col] = MINE;
		mine_exploded = true;
	}
	if (has_mine[row][col] == false) {
		int count = 0;
		//计算周边雷数(做法:以自身为中心(去除自身位置)循环3*3个位置)
		for (int k = row - 1; k <= row + 1; k++) {
			for (int l = col - 1; l <= col + 1; l++) {
				if (k >= 0 && k < game_stats[0] && l >= 0 && l < game_stats[1] && !(k == row && l == col)) {
					if (has_mine[k][l] == true)
						count++;
				}
			}
		}

		switch (count) {
		case 0:
			grid[row][col] = ZERO;
			break;
		case 1:
			grid[row][col] = ONE;
			break;
		case 2:
			grid[row][col] = TWO;
			break;
		case 3:
			grid[row][col] = THREE;
			break;
		case 4:
			grid[row][col] = FOUR;
			break;
		case 5:
			grid[row][col] = FIVE;
			break;
		case 6:
			grid[row][col] = SIX;
			break;
		case 7:
			grid[row][col] = SEVEN;
			break;
		case 8:
			grid[row][col] = EIGHT;
			break;
		}
		if (count == 0) {
			for (int k = row - 1; k <= row + 1; k++) {
				for (int l = col - 1; l <= col + 1; l++) {
					if (k >= 0 && k < game_stats[0] && l >= 0 && l < game_stats[1] && !(k == row && l == col) && is_revealed(k, l) == false) {
						reveal(k, l);
					}
				}
			}
		}
	}
}

// Implement the flag() function of Class
void Mine_Sweeper::flag(int row, int col)
{
	if (grid[row][col] == HIDDEN) {
		grid[row][col] = FLAGGED;
		game_stats[2]--;
		if (has_mine[row][col] == false)
			game_stats[3]++;
		return;
	}
	if (grid[row][col] == FLAGGED) {
		grid[row][col] = HIDDEN;
		game_stats[2]++;
		if (has_mine[row][col] == false)
			game_stats[3]--;
		return;
	}
}

void generate_grid(Mine_Sweeper& my_mine_sweeper) {
	cout << "Please input the following:" << '\n';
	do {
		cout << "Number of rows (5-25): ";
		cin >> my_mine_sweeper.game_stats[0];
	} while (my_mine_sweeper.game_stats[0] < 5 || my_mine_sweeper.game_stats[0] > 25);

	do {
		cout << "Number of cols (5-25): ";
		cin >> my_mine_sweeper.game_stats[1];
	} while (my_mine_sweeper.game_stats[1] < 5 || my_mine_sweeper.game_stats[1] > 25);

	for (int row = 0; row < my_mine_sweeper.game_stats[0]; row += 1) {
		for (int col = 0; col < my_mine_sweeper.game_stats[1]; col += 1) {
			my_mine_sweeper.grid[row][col] = HIDDEN;
		}
	}

	do {
		cout << "Number of mines (1 mine - 20% mines): ";
		cin >> my_mine_sweeper.game_stats[2];
	} while ((my_mine_sweeper.game_stats[2] < 1) ||
		(5 * my_mine_sweeper.game_stats[2] > my_mine_sweeper.game_stats[0] * my_mine_sweeper.game_stats[1]));
	my_mine_sweeper.game_stats[3] = 0;

	// Pseudo-random Mine Placement.
	srand(SEED);
	for (int n = 0; n < my_mine_sweeper.game_stats[2]; n++) {
		int row = rand() % my_mine_sweeper.game_stats[0];
		int col = rand() % my_mine_sweeper.game_stats[1];

		// If already have a mine in this location, increment col and wrap-around in row-major order.
		while (my_mine_sweeper.has_mine[row][col]) {
			row = (row + ((col + 1) / my_mine_sweeper.game_stats[1])) % my_mine_sweeper.game_stats[0];
			col = (col + 1) % my_mine_sweeper.game_stats[1];
		}
		my_mine_sweeper.has_mine[row][col] = true;
	}
}

bool reveal_cell(Mine_Sweeper& my_mine_sweeper) {
	char col_letter;
	int row, col;
	cout << "Please enter cell coordinates: ";
	cin >> col_letter;
	cin >> row;
	col = int(col_letter - 'A');
	row = row - 1;

	if (row < 0 || row >= my_mine_sweeper.get_num_rows() ||
		col < 0 || col >= my_mine_sweeper.get_num_cols()) {
		cout << "Given coordinates are out of bounds!" << '\n';
		return false;
	}
	if (my_mine_sweeper.is_revealed(row, col)) {
		cout << "Selected cell is already revealed!" << '\n';
		return false;
	}
	if (my_mine_sweeper.is_flagged(row, col)) {
		cout << "Selected cell is currently flagged!" << '\n';
		return false;
	}

	my_mine_sweeper.reveal(row, col);
	return true;
}

bool toggle_flag(Mine_Sweeper& my_mine_sweeper) {
	char col_letter;
	int row, col;
	cout << "Please enter cell coordinates: ";
	cin >> col_letter;
	cin >> row;
	col = int(col_letter - 'A');
	row = row - 1;

	if (row < 0 || row >= my_mine_sweeper.get_num_rows() ||
		col < 0 || col >= my_mine_sweeper.get_num_cols()) {
		cout << "Given coordinates are out of bounds!" << '\n';
		return false;
	}

	if (my_mine_sweeper.is_revealed(row, col)) {
		cout << "Selected cell is already revealed!" << '\n';
		return false;
	}

	my_mine_sweeper.flag(row, col);
	if (my_mine_sweeper.get_num_flags_left() < 0) {
		cout << "WARNING: Too many flags on the grid!" << '\n';
	}
	return true;
}

int main() {
	Mine_Sweeper my_mine_sweeper;

	cout << "MINESWEEPER!" << '\n';
	cout << '\n';

	generate_grid(my_mine_sweeper);

	// Game Loop.
	bool is_submitted = false;
	while (!is_submitted && !my_mine_sweeper.is_mine_exploded()) {
		my_mine_sweeper.display_grid();

		// Player Action Loop.
		bool valid_input = false;
		while (!valid_input) {
			cout << "Choose one of the following actions:" << '\n';
			cout << "0: Reveal cell" << '\n';
			cout << "1: Toggle flag" << '\n';
			cout << "2: Submit" << '\n';
			int player_action;
			cin >> player_action;

			switch (player_action) {
			case 0:
				valid_input = reveal_cell(my_mine_sweeper);
				break;
			case 1:
				valid_input = toggle_flag(my_mine_sweeper);
				break;
			case 2:
				valid_input = true;
				is_submitted = true;
				break;
			default:
				valid_input = false;
				cout << "Invalid input. Please enter again.\n" << '\n';
				break;
			}
		}
	}

	my_mine_sweeper.display_answer();

	if (!my_mine_sweeper.is_succeeded()) {
		cout << "WRONG FLAGGED! GAME OVER! YOU LOSE!" << '\n';
	}
	else if (my_mine_sweeper.is_mine_exploded()) {
		cout << "A MINE EXPLODED! GAME OVER! YOU LOSE!" << '\n';
	}
	else {
		cout << "CONGRATULATIONS! YOU WIN!" << '\n';
	}

	cout << endl;
	cout << "Press [ENTER] to exit..." << endl;
	cin.get();

	return 0;
}
```

## 大致效果

![img](https://pic1.zhimg.com/80/v2-00cf46608b4a51d2c8df9a9e77ab9b19_720w.png?source=d16d100b)

