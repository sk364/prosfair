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
    vector<int> temp(64, 0);

    for (int i=0; i < 32; i++) {
        int x = find_pos(board[i]) % 8, y = find_pos(board[i]) / 8;
        temp[y * 8 + x] = i;
    }

    for (int i=0; i < 8; i++, putchar('\n'))
        for (int j=0; j < 8; j++, putchar(' '))
            cout << temp[i * 8 + j];
}


void print_vec_bitboard(vector<llu> v) {
    for (int i=0; i < v.size(); i++)
        print_bitboard(v[i]);
    cout << endl;
}


void print_move_vector(vector<move_piece> v) {
    for(int i=0; i < v.size(); i++)
        cout << v[i].piece << " " << v[i].x << " "<< v[i].y << " , ";
    cout << endl;
}

  
inline llu hasher(vector<llu> &v) {
    llu hash = 0;

    for (int i=0; i < v.size(); i++)
        hash = v[i] + 0x9e3779b9 + hash << 6 + hash >> 2;

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

    for (int i=PAWN1; i <= PAWN8; i++)
        if (piece == i)
            return 10;

    for (int i=OPAWN1; i <= OPAWN8; i++)
        if (piece == i)
            return 10;
    return 0;
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
    if (p < 0) return return_llu();

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
    int p = find_pos(b);
    int x = p % 8;
    int y = p / 8;
    if (p < 0) return return_llu();

    llu res = 0;

    if (dir) {
        if (y + 1 >= 0 and y + 1 <= 7) {
            if (not attack)
                res |= set_bit(x , y + 1);
            if (attack)
                res |= set_bit(x - 1, y + 1);
            if (attack)
                res |= set_bit(x + 1, y + 1);
        }
    } else {
        if (y - 1 >= 0 and y - 1 <= 7) {
            if (not attack)
                res |= set_bit(x, y - 1);
            if (attack)
                res |= set_bit(x - 1, y - 1);
            if (attack)
                res |= set_bit(x + 1, y - 1);
        }
    }

    return res;
}


llu find_enemy_occupied_area(vector<llu> &board, int piece) {
    llu occupied_enemy_area = 0;

    for (int i=(piece < OKING ? OKING : KING); i <= (piece < OKING ? OPAWN8 : PAWN8); i++) {
        cout << occupied_enemy_area << endl;
        occupied_enemy_area |= board[i];
    }

    return occupied_enemy_area;
}


llu find_friend_occupied_area(vector<llu> &board, int piece) {
    llu occupied_friend_area = 0;

    for (int i=(piece < OKING ? KING : OKING); i <= (piece < OKING ? PAWN8 : OPAWN8); i++)
        occupied_friend_area |= board[i];

    return occupied_friend_area;
}


llu pawn_moves_wrapper(vector<llu> &board, int pawn) {
    llu pawn_attack_board = moves_pawn(board[pawn], pawn < OKING ? true : false, true);
    llu occupied_enemy_area = find_enemy_occupied_area(board, pawn);
    llu occupied_friend_area = find_friend_occupied_area(board, pawn);
    pawn_attack_board = occupied_enemy_area & pawn_attack_board;
    llu pawn_move_board = (
        moves_pawn(board[pawn], pawn < OKING ? true : false, false) & (~occupied_friend_area & ~occupied_enemy_area));

    return pawn_attack_board | pawn_move_board;
}


bool if_piece_under_attack(vector<llu> & board, int piece) {
    llu enemy_attack_area = 0;

    for (int i=piece < OKING ? OKING : KING; i <= piece < OKING ? OPAWN8 : PAWN8; i++)
        enemy_attack_area |= moves_wrapper(board, i);

    if (enemy_attack_area & board[piece])
        return true;
    else
        return false;
}


bool in_check(vector<llu> & board, int king) {
    return if_piece_under_attack(board, king);
}


bool in_checkmate(vector<llu> & board, int king) {
    if (!in_check(board,king)) return false;

    vector<move_piece> moves = get_all_moves(board, king);

    for (int i=0 ; i < moves.size(); i++) {
        vector<llu> temp_board = generate_board(board,moves[i]);
        if(!in_check(temp_board,king))
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

    for (int i=0; i < 16; i++)
        moves[i] = moves_wrapper(board, army_king + i);

    return moves;
}


vector<move_piece> get_all_moves(vector<llu> &board, int army_king) {
    vector<move_piece> ret_v;
    vector<llu> moves_bit = find_moves(board, army_king);

    for (int i=0; i < 16; i++) {
        vector<move_piece> moves_list = get_move_vector(moves_bit[i], i + army_king);
        ret_v.insert(ret_v.end(), moves_list.begin(), moves_list.end());
    }

    return ret_v;
}


vector<llu> generate_board(vector<llu> & board,move_piece m) {
    vector<llu> new_board(board);
    for (int i=(m.piece < OKING ? OKING : KING); i <= ((m.piece < OKING) ? OPAWN8 : PAWN8); i++) {
        if (m.x == find_pos(new_board[i]) % 8 and m.y == find_pos(new_board[i]) / 8 ) {
            new_board[i] = 0;
            break;
        }
    }

    new_board[m.piece] = set_bit(m.x, m.y);
    return new_board;
}


float evaluate_board(vector<llu> &board, int army_king) {
    llu board_hash = hash_pair(hasher(board), army_king);

    if (evaluate_board_memo.find(board_hash) != evaluate_board_memo.end())
        return evaluate_board_memo[board_hash];
    else {
        if (in_checkmate(board, army_king)) {
            return evaluate_board_memo[board_hash] = (float)-99999;
        }
        if (in_checkmate(board, army_king < OKING ? OKING : KING)) {
            return evaluate_board_memo[board_hash] = (float)99999;
        }

        float sum = 0.0;
        for(int i = KING; i < OKING; i++)
            sum += ((board[i] != return_llu()) - (board[i + OKING] != return_llu())) *piece_priority(i);

        return evaluate_board_memo[board_hash] = sum;
    }
}


move_piece alpha_beta(vector<llu> &board, int army_king, int depth) {
    vector<move_piece> moves_list = get_all_moves(board, army_king);
    if (depth <= 0 or moves_list.size() == 0)
        return (move_piece){-1, 0, 0};

    float best_score = -99999;
    float alpha = -99999, beta = 99999;
    move_piece best_move = moves_list[0];

    for (int i=0; i < moves_list.size(); i++) {
        cout << moves_list[i].piece << " " << moves_list[i].x << " " << moves_list[i].y << endl;
        // vector<llu> clone_board = generate_board(board, moves_list[i]);
        // float score = alpha_beta_min(clone_board, army_king < OKING ? OKING : KING, alpha, beta, depth - 1);

        // if (score > best_score) {
        //     best_move = moves_list[i];
        //     best_score = score;
        // }
    }

    return best_move;
}

    
float alpha_beta_min(vector<llu> &board, int army_king, float alpha, float beta, int depth) {
    if (depth == 0)
        return -evaluate_board(board, army_king);

    llu board_hash = hasher(board);

    if (min_play_memo.find(board_hash) != min_play_memo.end())
        return min_play_memo[board_hash];
    else {
        vector<move_piece> moves_list = get_all_moves(board, army_king);

        if (moves_list.size() == 0)
            return -evaluate_board(board, army_king);

        float _alpha = alpha;
        float _beta = beta;
        float score = 99999;

        for (int i=0; i < moves_list.size(); i++) {
            vector<llu> clone_board = generate_board(board, moves_list[i]);
            float score = min(
                score,
                alpha_beta_max(clone_board, army_king < OKING ? OKING : KING, _alpha, _beta, depth - 1)
            );

            _beta = min(score, _beta);
            if (_beta <= _alpha)
                return min_play_memo[board_hash] = score;   
        }
        return min_play_memo[board_hash] = score;
    }
}

    
float alpha_beta_max(vector<llu> &board, int army_king, float alpha, float beta, int depth) {
    if (depth == 0)
        return evaluate_board(board, army_king);

    llu board_hash = hasher(board);

    if (max_play_memo.find(board_hash) != max_play_memo.end())
        return max_play_memo[board_hash];
    else {
        vector<move_piece> moves_list = get_all_moves(board, army_king);

        if (moves_list.size() == 0)
            return evaluate_board(board, army_king);

        float _alpha = alpha;
        float _beta = beta;
        float score = -99999;

        for (int i=0; i < moves_list.size(); i++) {
            vector<llu> clone_board = generate_board(board, moves_list[i]);
            float score = max(
                score,
                alpha_beta_min(clone_board, army_king < OKING ? OKING : KING, _alpha, _beta, depth - 1)
            );
            _alpha = max(score, _alpha);

            if (_beta >= _alpha)
                return max_play_memo[board_hash] = score;   
        }
        return max_play_memo[board_hash] = score;
    }
}


int main(int argc, char *argv[]) {
    vector<llu> bb(32, 0);

    int depth = atoi(argv[1]);

    for (int i=0; i < 32; i++) {
        int x, y;
        cin >> y >> x;

        if (x > -1 and y > -1)
            bb[i] = set_bit(x, y);
        else
            bb[i] = return_llu();
    }

    move_piece ans = alpha_beta(bb, OKING, depth);
    cout << ans.piece << " " << ans.x << " " << ans.y << endl;

    return 0;
}
