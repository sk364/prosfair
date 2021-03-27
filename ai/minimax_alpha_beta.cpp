#include<bits/stdc++.h>

using namespace std;

struct move_structure{
    int piece;
    int x;
    int y;
};

typedef struct move_structure move_piece;

#define llu long long unsigned int
#define KING    0
#define QUEEN   1
#define BISHOP1 2
#define BISHOP2 3
#define KNIGHT1 4
#define KNIGHT2 5
#define ROOK1   6
#define ROOK2   7
#define PAWN1   8
#define PAWN8  15

#define OKING   16
#define OQUEEN  17
#define OBISHOP1 18
#define OBISHOP2 19
#define OKNIGHT1 20
#define OKNIGHT2 21
#define OROOK1   22
#define OROOK2  23
#define OPAWN1  24
#define OPAWN8  31

map<llu, float> min_play_memo;
map<llu, float> max_play_memo;
map<llu, float> evaluate_board_memo;

llu hash_pair(llu, llu);

move_piece alpha_beta(vector<llu> &, int, int);
float alpha_beta_min(vector<llu> &, int, float, float, int);
float alpha_beta_max(vector<llu> &, int, float, float, int);

float min_play(vector<llu>, int, int);
float max_play(vector<llu>, int, int);
float evaluate_board(vector<llu> &, int);
llu set_bit(int, int);
llu find_friend_occupied_area(vector<llu> &, int);
llu find_enemy_occupied_area(vector<llu> &, int);
llu moves_bishop(vector<llu> &, llu);
llu moves_rook(vector<llu> &, llu);
llu moves_king(llu);
llu moves_knight(llu);
llu moves_queen(vector<llu> &, llu);
llu moves_wrapper(vector<llu> &, int);
llu moves_wrapper_2(vector<llu> &, int);
llu pawn_moves_wrapper(vector<llu> &, int);
llu return_llu();
llu return_one();
inline llu hasher(vector<llu> &);
vector<move_piece> get_all_moves(vector<llu> &, int);
vector<llu> generate_board(vector<llu> &, move_piece);

float PAWN_SQUARE_TABLE[8][8] = {
    {0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0},
    {5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0},
    {1.0,  1.0,  2.0,  3.0,  3.0,  2.0,  1.0,  1.0},
    {0.5,  0.5,  1.0,  2.5,  2.5,  1.0,  0.5,  0.5},
    {0.0,  0.0,  0.0,  2.0,  2.0,  0.0,  0.0,  0.0},
    {0.5, -0.5, -1.0,  0.0,  0.0, -1.0, -0.5,  0.5},
    {0.5,  1.0, 1.0,  -2.0, -2.0,  1.0,  1.0,  0.5},
    {0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0}
};

float KNIGHT_SQUARE_TABLE[8][8] = {
    {-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0},
    {-4.0, -2.0,  0.0,  0.0,  0.0,  0.0, -2.0, -4.0},
    {-3.0,  0.0,  1.0,  1.5,  1.5,  1.0,  0.0, -3.0},
    {-3.0,  0.5,  1.5,  2.0,  2.0,  1.5,  0.5, -3.0},
    {-3.0,  0.0,  1.5,  2.0,  2.0,  1.5,  0.0, -3.0},
    {-3.0,  0.5,  1.0,  1.5,  1.5,  1.0,  0.5, -3.0},
    {-4.0, -2.0,  0.0,  0.5,  0.5,  0.0, -2.0, -4.0},
    {-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0}
};

float BISHOP_SQUARE_TABLE[8][8] = {
    { -2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0},
    { -1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0},
    { -1.0,  0.0,  0.5,  1.0,  1.0,  0.5,  0.0, -1.0},
    { -1.0,  0.5,  0.5,  1.0,  1.0,  0.5,  0.5, -1.0},
    { -1.0,  0.0,  1.0,  1.0,  1.0,  1.0,  0.0, -1.0},
    { -1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0, -1.0},
    { -1.0,  0.5,  0.0,  0.0,  0.0,  0.0,  0.5, -1.0},
    { -2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0}
};

float QUEEN_SQUARE_TABLE[8][8] = {
    { -2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0},
    { -1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0},
    { -1.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0},
    { -0.5,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5},
    {  0.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5},
    { -1.0,  0.5,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0},
    { -1.0,  0.0,  0.5,  0.0,  0.0,  0.0,  0.0, -1.0},
    { -2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0}
};

float ROOK_SQUARE_TABLE[8][8] = {
    {  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0},
    {  0.5,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  0.5},
    { -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5},
    { -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5},
    { -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5},
    { -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5},
    { -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5},
    {  0.0,   0.0, 0.0,  0.5,  0.5,  0.0,  0.0,  0.0}
};

float KING_SQUARE_TABLE[8][8] = {
    { -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0},
    { -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0},
    { -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0},
    { -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0},
    { -2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0},
    { -1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0},
    {  2.0,  2.0,  0.0,  0.0,  0.0,  0.0,  2.0,  2.0 },
    {  2.0,  3.0,  1.0,  0.0,  0.0,  1.0,  3.0,  2.0 }
};

int cpu_player = 16;


int opposite(int army) {
    return army < OKING ? OKING : KING;
}


int find_pos(llu x) {
    int i = 0;
    for (int i=0; i < 64; i++)
        if(((x>>i) & 1) == 1)
            return i;

    return -1;
}


void print_bitboard(llu x) {
    int i = 0;

    for (int i=0; i < 8; i++, printf("\n"))
        for(int j=0; j < 8; j++)
            printf("%c", (char)('0' + ((x >> (i * 8 + j)) & 1)));

    printf("\n");
}


void pretty_print_board(vector<llu> board) {
    vector<int> temp(64, -1);

    for (int i=0; i < 32; i++) {
        int x = find_pos(board[i]) % 8, y = find_pos(board[i]) / 8;
        temp[y * 8 + x] = i;
    }

    for (int i=0; i < 8; i++, putchar('\n')) {
        for (int j=0; j < 8; j++, putchar(' ')) {
            if (temp[i * 8 + j] == -1)
                cout << "__";
            else {
                if (temp[i * 8 + j] < 10 or temp[i * 8 + j] == 16)
                    cout << "0";

                if (temp[i * 8 + j] != 0 and temp[i * 8 + j] != 16)
                    cout << temp[i * 8 + j];
                else
                    cout << "K";
            }
        }
    }
}


void print_vec_bitboard(vector<llu> v) {
    for (int i=0; i < v.size(); i++)
        print_bitboard(v[i]);
    cout << endl;
}


void print_move_vector(vector<move_piece> v) {
    for(int i=0; i < v.size(); i++)
        cout << v[i].piece << " " << v[i].y << " "<< v[i].x << " | ";
    cout << endl;
}


void print_binary(llu x) {
    bool binary[64];
    int rem;
    int i = 0;
    llu temp = x;

    for (i = 0; i < 64; i++) {
        binary[i] = false;
    }

    i = 0;
    while (x > 0) {
        binary[i++] = x % 2;
        x /= 2;
    }

    cout << temp << endl;
    for (i = 63; i > -1; i--) {
        cout << binary[i];
    }

    cout << endl << endl;
}

  
inline llu hasher(vector<llu> &v) {
    llu hash = 0;

    for (int i=0; i < v.size(); i++)
        hash = v[i] + 0x9e3779b9 + (hash << 6) + (hash >> 2);

    return hash;
}


inline llu hash_pair(llu a, llu b) {
    vector<llu> v;
    v.push_back(a);
    v.push_back(b);
    return hasher(v);
}


inline float piece_priority(int piece) {
    switch(piece) {
        case KING:  
        case OKING: return 900;
        
        case QUEEN:     
        case OQUEEN: return 90;

        case BISHOP1:
        case BISHOP2:
        case OBISHOP1:
        case OBISHOP2: return 30;

        case KNIGHT1:
        case KNIGHT2:
        case OKNIGHT1:
        case OKNIGHT2: return 30;

        case ROOK1:
        case ROOK2:
        case OROOK1:
        case OROOK2: return 50;
    }

    if (piece >= PAWN1 and piece <= PAWN8)
        return 10;

    if (piece >= OPAWN1 and piece <= OPAWN8)
        return 10;

    return 0;
}


inline float piece_position_value(int piece, llu position) {
    int p = find_pos(position);
    if (p < 0) return 0.0;

    int y = p / 8;
    int x = p % 8;

    if (cpu_player == 16) {
        y = 7 - y;
        x = 7 - x;
    }

    switch(piece) {
        case KING:  
        case OKING: return KING_SQUARE_TABLE[y][x];
        
        case QUEEN:     
        case OQUEEN: return QUEEN_SQUARE_TABLE[y][x];

        case BISHOP1:
        case BISHOP2:
        case OBISHOP1:
        case OBISHOP2: return BISHOP_SQUARE_TABLE[y][x];

        case KNIGHT1:
        case KNIGHT2:
        case OKNIGHT1:
        case OKNIGHT2: return KNIGHT_SQUARE_TABLE[y][x];

        case ROOK1:
        case ROOK2:
        case OROOK1:
        case OROOK2: return ROOK_SQUARE_TABLE[y][x];
    }

    if ((piece >= PAWN1 and piece <= PAWN8) or (piece >= OPAWN1 and piece <= OPAWN8))
        return PAWN_SQUARE_TABLE[y][x];

    return 0.0;
}


llu set_bit(int x, int y) {
    if (y >= 0 and y <= 7 and x >= 0 and x <= 7)
        return (return_llu() | (return_one()) << (8 * y + x));
    return return_llu();
}


llu return_llu() {
    llu x = 0;
    return x;
}


llu return_one() {
    llu x = 1;
    return x;
}


llu moves_wrapper(vector<llu> &b, int piece) {
    return (~find_friend_occupied_area(b, piece)) & moves_wrapper_2(b, piece);
}


llu moves_wrapper_2(vector<llu> &b, int piece) {
    switch(piece) {
        case KING:  return moves_king(b[KING]);
        case OKING: return moves_king(b[OKING]);
        
        case QUEEN:  return moves_queen(b, b[QUEEN]);
        case OQUEEN: return moves_queen(b, b[OQUEEN]);

        case BISHOP1: return moves_bishop(b, b[BISHOP1]);
        case BISHOP2: return moves_bishop(b, b[BISHOP2]);

        case OBISHOP1: return moves_bishop(b, b[OBISHOP1]);
        case OBISHOP2: return moves_bishop(b, b[OBISHOP2]);

        case KNIGHT1:  return moves_knight(b[KNIGHT1]);
        case KNIGHT2:  return moves_knight(b[KNIGHT2]);
        case OKNIGHT1: return moves_knight(b[OKNIGHT1]);
        case OKNIGHT2: return moves_knight(b[OKNIGHT2]);

        case ROOK1:  return moves_rook(b, b[ROOK1]);
        case ROOK2:  return moves_rook(b, b[ROOK2]);
        case OROOK1: return moves_rook(b, b[OROOK1]);
        case OROOK2: return moves_rook(b, b[OROOK2]);
    }

    for (int i=PAWN1; i <= PAWN8; i++)
        if (piece == i)
            return pawn_moves_wrapper(b, i);

    for (int i=OPAWN1; i <= OPAWN8; i++)
        if (piece == i)
            return pawn_moves_wrapper(b, i);

    return return_llu();
}


llu moves_king(llu b) {
    int p  = find_pos(b);
    if (p < 0)
        return return_llu();

    int x = p % 8;
    int y = p / 8;

    llu res = 0;

    for (int i=-1; i <= 1; i++)
        for(int j=-1; j <= 1; j++)
            if (not (i==j and i == 0))
                res |= set_bit(x + i, y + j);

    return res;
}


llu moves_queen(vector<llu> &board, llu b) {
    return moves_bishop(board, b) | moves_rook(board, b);
}


llu moves_bishop(vector<llu> &board, llu b) {
    int p = find_pos(b);
    int x = p % 8;
    int y = p / 8;
    if (p < 0) return 0LLU;

    llu res = 0;

    for (int i=0; i >= -7; i--) {
        if (not (i == 0)) {
            if (set_bit(x + i, y + i) & (find_friend_occupied_area(board, b)))
                break;

            res |= set_bit(x + i, y + i);

            if(set_bit(x + i, y + i) & (find_enemy_occupied_area(board, b)))
                break;
        }
    }


    for (int i=0; i >= -7; i--) {
        if (not (i == 0)) {
            if (set_bit(x + i, y - i) & (find_friend_occupied_area(board, b)))
                break;

            res |= set_bit(x+i,y-i);

            if (set_bit(x + i, y - i) & (find_enemy_occupied_area(board, b)))
                break;
        }
    }


    for (int i =0; i <= 7; i++) {
        if (not (i == 0)) {
            if (set_bit(x + i, y + i) & (find_friend_occupied_area(board, b)))
                break;

            res |= set_bit(x + i, y + i);

            if (set_bit(x + i, y + i) & (find_enemy_occupied_area(board, b)))
                break;

        }
    }


    for (int i=0; i <= 7; i++) {
        if (not (i == 0)) {
            if (set_bit(x + i, y - i) & (find_friend_occupied_area(board, b)))
                break;

            res |= set_bit(x+i,y-i);

            if (set_bit(x + i, y - i) & (find_enemy_occupied_area(board, b)))
                break;
        }
    }

    return res;
}


llu moves_knight(llu b) {
    int p = find_pos(b);
    int x = p % 8;
    int y = p / 8;
    if (p < 0) return return_llu();

    llu res = 0;

    for(int i=-2; i <= 2; i+=2)
        for(int j=-1; j <= 1; j++) {
            if (not (j == 0 or i == 0))
                res |= set_bit(x + j, y + i);
            if (not (j == 0 or i == 0))
                res |= set_bit(x + i, y + j);
        }

    return res;
}


llu moves_rook(vector<llu> &board, llu b) {
    int p =  find_pos(b);
    int x = p % 8;
    int y = p / 8;
    if (p < 0) return return_llu();

    llu res = 0;

    for (int i=0; i >= -7; i--) {
        if (not (i == 0)) {
            if (set_bit(x + i, y) & (find_friend_occupied_area(board, b)))
                break;

            res |= set_bit(x + i, y);

            if (set_bit(x + i, y) & (find_enemy_occupied_area(board, b)) )
                break;
        }
    }

    for (int i=0; i >= -7; i--) {
        if (not (i == 0)) {
            if (set_bit(x, y + i) & (find_friend_occupied_area(board, b)))
                break;

            res |= set_bit(x, y + i);

            if (set_bit(x, y + i) & (find_enemy_occupied_area(board, b)))
                break;
        }
    }


    for (int i=0; i <= 7; i++) {
        if (not (i == 0)) {
            if (set_bit(x + i, y) & (find_friend_occupied_area(board, b)))
                break;

            res |= set_bit(x + i, y);

            if (set_bit(x + i, y) & (find_enemy_occupied_area(board, b)))
                break;

        }
    }


    for (int i=0; i <= 7; i++) {
        if (not ( i == 0)) {
            if (set_bit(x, y + i) & (find_friend_occupied_area(board, b))) break;

            res |= set_bit(x, y + i);

            if (set_bit(x, y + i) & (find_enemy_occupied_area(board, b)))
                break;
        }
    }

    return res;
}


llu moves_pawn(llu b, bool dir, bool attack) {
    // TODO: en passant
    int p = find_pos(b);
    int x = p % 8;
    int y = p / 8;
    if (p < 0) return return_llu();

    llu res = 0;

    if (!dir) {
        if (y + 1 >= 0 and y + 1 <= 7) {
            if (attack) {
                res |= set_bit(x - 1, y + 1);
                res |= set_bit(x + 1, y + 1);
            } else {
                res |= set_bit(x , y + 1);
            }
        }
    } else {
        if (y - 1 >= 0 and y - 1 <= 7) {
            if (attack) {
                res |= set_bit(x - 1, y - 1);
                res |= set_bit(x + 1, y - 1);
            } else {
                res |= set_bit(x, y - 1);
            }
        }
    }

    return res;
}


llu moves_pawn_double_jump(llu b, bool dir, llu pawn_move_board) {
    int p = find_pos(b);
    int x = p % 8;
    int y = p / 8;
    if (p < 0) return return_llu();

    if (!dir) {
        if (y == 1) {
            llu one_step = set_bit(x, y + 1);
            llu can_double = pawn_move_board & one_step;
            if (can_double) {
                return set_bit(x, y + 2);
            }
        }
    } else {
        if (y == 6) {
            llu one_step = set_bit(x, y - 1);
            llu can_double = pawn_move_board & one_step;
            if (can_double) {
                return set_bit(x, y - 2);
            }
        }
    }

    return return_llu();
}


llu find_enemy_occupied_area(vector<llu> &board, int piece) {
    llu occupied_enemy_area = 0;

    for (int i=opposite(piece); i <= (piece < OKING ? OPAWN8 : PAWN8); i++) {
        occupied_enemy_area |= board[i];
    }

    return occupied_enemy_area;
}


llu find_friend_occupied_area(vector<llu> &board, int piece) {
    llu occupied_friend_area = 0;

    for (int i=opposite(piece); i <= (piece < OKING ? PAWN8 : OPAWN8); i++)
        occupied_friend_area |= board[i];

    return occupied_friend_area;
}


llu pawn_moves_wrapper(vector<llu> &board, int pawn) {
    llu pawn_attack_board = moves_pawn(board[pawn], pawn < OKING ? true : false, true);
    llu occupied_enemy_area = find_enemy_occupied_area(board, pawn);
    llu occupied_friend_area = find_friend_occupied_area(board, pawn);
    pawn_attack_board = occupied_enemy_area & pawn_attack_board;
    llu pawn_move_board = (
        moves_pawn(board[pawn], pawn < OKING ? true : false, false) &
        ~occupied_friend_area &
        ~occupied_enemy_area
    );
    llu pawn_double_jump_board = (
        moves_pawn_double_jump(board[pawn], pawn < OKING ? true : false, pawn_move_board) &
        ~occupied_enemy_area &
        ~occupied_friend_area
    );

    return pawn_attack_board | pawn_move_board | pawn_double_jump_board;
}


bool if_piece_under_attack(vector<llu> & board, int piece) {
    llu enemy_attack_area = 0;

    for (int i=opposite(piece); i <= (piece < OKING ? OPAWN8 : PAWN8); i++)
        enemy_attack_area |= moves_wrapper(board, i);

    if (enemy_attack_area & board[piece])
        return true;
    else
        return false;
}


bool in_check(vector<llu> & board, int king) {
    return if_piece_under_attack(board, king);
}


bool in_checkmate(vector<llu> &board, int king) {
    if (!in_check(board, king)) return false;

    vector<move_piece> moves = get_all_moves(board, king);

    for (int i=0 ; i < moves.size(); i++) {
        vector<llu> temp_board = generate_board(board, moves[i]);
        if(!in_check(temp_board, king))
            return false;
    }

    return true; 
}


vector<move_piece> get_move_vector(llu b, int piece) {
    vector<move_piece> v;

    for (int y=0; y < 8; y++)
        for (int x=0; x < 8; x++)
            if ((b >> (8 * y + x)) & 1)
                v.push_back((move_piece){ piece, x, y});

    return v;
}


vector<llu> find_moves(vector<llu> & board, int army_king) {
    vector<llu>  moves(16, return_llu());

    for (int i=0; i < 16; i++) {
        moves[i] = moves_wrapper(board, army_king + i);
    }

    return moves;
}


vector<move_piece> get_all_moves(vector<llu> &board, int army_king) {
    vector<move_piece> ret_v;
    vector<llu> moves_bit = find_moves(board, army_king);

    for (int i=0; i < 16; i++) {
        vector<move_piece> moves_list = get_move_vector(moves_bit[i], i + army_king);
        vector<move_piece> _moves;
        for (int j=0; j < moves_list.size(); j++) {
            vector<llu> clone_board = generate_board(board, moves_list[j]);
            if (!in_check(clone_board, army_king)) {
                _moves.push_back(moves_list[j]);
            }
        }

        ret_v.insert(ret_v.end(), _moves.begin(), _moves.end());
    }

    return ret_v;
}


vector<llu> generate_board(vector<llu> &board, move_piece m) {
    // TODO: check if move is castling or not or pawn is promoted or not or pawn kills another pawn by en passant
    vector<llu> new_board(board);
    for (int i=opposite(m.piece); i <= ((m.piece < OKING) ? OPAWN8 : PAWN8); i++) {
        if (m.x == find_pos(new_board[i]) % 8 and m.y == find_pos(new_board[i]) / 8 ) {
            new_board[i] = 0;
            break;
        }
    }

    new_board[m.piece] = set_bit(m.x, m.y);
    return new_board;
}


float sum_of_pieces(vector<llu> board, int army_king) {
    float sum = 0.0;
    for (int i=army_king; i <= (army_king < OKING ? PAWN8 : OPAWN8); i++) {
        if (board[i] != 0) {
            sum += (piece_priority(i) + piece_position_value(i, board[i]));
        }
    }
    return sum;
}


int compute_mobility(vector<llu> board, int army_king) {
    vector<move_piece> moves_list = get_all_moves(board, army_king);
    return moves_list.size();
}


int count_doubled_pawns(vector<llu> board, int army_king) {
    int doubled_pawns = 0;
    for (int i=8 + army_king; i <= (army_king < OKING ? PAWN8 : OPAWN8); i++) {
        int pos = find_pos(board[i]);
        if (pos < 0)
            continue;

        int y = pos / 8;
        int x = pos % 8;

        llu one_step_ahead = set_bit(x, y + 1);
        llu one_step_back = set_bit(x, y - 1);
        for (int j=8 + army_king; j <= (army_king < OKING ? PAWN8: OPAWN8); j++) {
            if (i != j) {
                if (one_step_ahead == board[j] or one_step_back == board[j]) {
                    doubled_pawns++;
                    break;
                }
            }
        }
    }

    return doubled_pawns;
}


int count_blocked_pawns(vector<llu> board, int army_king) {
    int blocked_pawns = 0;
    for (int i=8 + army_king; i <= (army_king < OKING ? PAWN8 : OPAWN8); i++) {
        int pos = find_pos(board[i]);
        if (pos < 0)
            continue;

        int y = pos / 8;
        int x = pos % 8;

        int one_step_ahead = cpu_player != army_king ? y + 1 : y - 1;
        llu pos_one_ahead = set_bit(x, one_step_ahead);
        for (int j=opposite(army_king); j < 16 + opposite(army_king); j++) {
            if (board[j] == pos_one_ahead) {
                llu pos_left_dia = set_bit(x - 1, one_step_ahead);
                llu pos_right_dia = set_bit(x + 1, one_step_ahead);

                bool exists = false;
                for (int k=opposite(army_king); k < 16 + opposite(army_king); k++) {
                    if (board[k] == pos_left_dia or board[k] == pos_right_dia) {
                        exists = true;
                        break;
                    }
                }
                if (!exists) {
                    blocked_pawns++;
                }
            }
        }
    }

    return blocked_pawns;
}


tuple <int, int> count_misc_pawns(vector<llu> board, int army_king) {
    int isolated_pawns = 0;
    int connected_pawns = 0;

    for (int i=8 + army_king; i <= (army_king < OKING ? PAWN8 : OPAWN8); i++) {
        int pos = find_pos(board[i]);
        if (pos < 0)
            continue;

        int y = pos / 8;
        int x = pos % 8;

        for (int j=-1; j <= 1; j++) {
            for (int k=-1; k <= 1; k++) {
                if (not (j == k and j == 0)) {
                    llu _pos = set_bit(x + j, y + k);
                    bool found = false;
                    for (int l=8 + army_king; l <= (army_king < OKING ? PAWN8 : OPAWN8); l++) {
                        if (l != i and _pos == board[l]) {
                            found = true;
                            break;
                        }
                    }
                    if (found) {
                        connected_pawns += 1;
                    } else {
                        isolated_pawns += 1;
                    }
                }
            }
        }
    }

    return make_pair(isolated_pawns, connected_pawns);
}


float evaluate_board(vector<llu> &board) {
    llu board_hash = hash_pair(hasher(board), cpu_player);

    if (evaluate_board_memo.find(board_hash) != evaluate_board_memo.end())
        return evaluate_board_memo[board_hash];
    else {
        if (in_checkmate(board, cpu_player))
            return -99999;
        if (in_checkmate(board, opposite(cpu_player)))
            return 99999;

        float sum_of_pieces1 = sum_of_pieces(board, cpu_player);
        float sum_of_pieces2 = sum_of_pieces(board, opposite(cpu_player));
        int mobility1 = compute_mobility(board, cpu_player);
        int mobility2 = compute_mobility(board, opposite(cpu_player));
        int num_doubled_pawns1 = count_doubled_pawns(board, cpu_player);
        int num_blocked_pawns1 = count_blocked_pawns(board, cpu_player);
        int num_isolated_pawns1, num_connected_pawns1;
        tie(num_isolated_pawns1, num_connected_pawns1) = count_misc_pawns(board, cpu_player);
        int num_doubled_pawns2 = count_doubled_pawns(board, opposite(cpu_player));
        int num_blocked_pawns2 = count_blocked_pawns(board, opposite(cpu_player));
        int num_isolated_pawns2, num_connected_pawns2;
        tie(num_isolated_pawns2, num_connected_pawns2) = count_misc_pawns(board, opposite(cpu_player));

        return evaluate_board_memo[board_hash] = (
            (sum_of_pieces1 - sum_of_pieces2) +
            (0.1 * (mobility1 - mobility2)) -
            (
                0.5 * (
                    (num_isolated_pawns1 - num_isolated_pawns2) +
                    (num_blocked_pawns1 - num_blocked_pawns2) +
                    (num_doubled_pawns1 - num_doubled_pawns2)
                )
            )
        );
    }
}


move_piece alpha_beta(vector<llu> &board, int army_king, int depth, float &best_score) {
    vector<move_piece> moves_list = get_all_moves(board, army_king);
    if (depth <= 0 or moves_list.size() == 0)
        return (move_piece){-1, 0, 0};

    float alpha = -99999, beta = 99999;
    move_piece best_move = moves_list[0];

    // print_move_vector(moves_list);
    for (int i=0; i < moves_list.size(); i++) {
        vector<llu> clone_board = generate_board(board, moves_list[i]);
        float score = alpha_beta_min(clone_board, opposite(army_king), alpha, beta, depth - 1);

        // cout << moves_list[i].piece << " " << moves_list[i].y << " " << moves_list[i].x << endl;
        // cout << score << endl << endl;
        if (score > best_score) {
            best_move = moves_list[i];
            best_score = score;
        }
    }

    return best_move;
}

    
float alpha_beta_min(vector<llu> &board, int army_king, float alpha, float beta, int depth) {
    if (depth == 0)
        return evaluate_board(board);

    llu board_hash = hasher(board);

    if (min_play_memo.find(board_hash) != min_play_memo.end())
        return min_play_memo[board_hash];

    vector<move_piece> moves_list = get_all_moves(board, army_king);

    float score = 99999;
    for (int i=0; i < moves_list.size(); i++) {
        vector<llu> clone_board = generate_board(board, moves_list[i]);
        score = alpha_beta_max(clone_board, opposite(army_king), alpha, beta, depth - 1);

        if (score <= alpha)
            return alpha;

        if (score < beta)
            beta = score;
    }
    return min_play_memo[board_hash] = beta;
}

    
float alpha_beta_max(vector<llu> &board, int army_king, float alpha, float beta, int depth) {
    if (depth == 0)
        return evaluate_board(board);

    llu board_hash = hasher(board);

    if (max_play_memo.find(board_hash) != max_play_memo.end())
        return max_play_memo[board_hash];

    vector<move_piece> moves_list = get_all_moves(board, army_king);

    float score = -99999;
    for (int i=0; i < moves_list.size(); i++) {
        vector<llu> clone_board = generate_board(board, moves_list[i]);
        score = alpha_beta_min(clone_board, opposite(army_king), alpha, beta, depth - 1);

        if (score >= beta)
            return beta;

        if (score > alpha)
            alpha = score;
    }
    return max_play_memo[board_hash] = alpha;
}


int main(int argc, char *argv[]) {
    vector<llu> bb(32, 0);

    int player = atoi(argv[1]);
    int depth = atoi(argv[2]);

    cpu_player = player;

    for (int i=0; i < 32; i++) {
        int x, y;
        cin >> y >> x;

        if (x > -1 and y > -1)
            bb[i] = set_bit(x, y);
        else
            bb[i] = return_llu();
    }
    // pretty_print_board(bb);

    float score = -99999;
    move_piece ans = alpha_beta(bb, player, depth, score);
    cout << find_pos(bb[ans.piece]) << " " << ans.piece << " " << ans.x << " " << ans.y << " " << score;

    return 0;
}
