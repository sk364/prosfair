// the use of -1 LLU as return value to show that there is no piece on the board is definately going to create a bug one day!!


#include<bits/stdc++.h>

using namespace std;

struct move_structure{
	int piece;
	int x;
	int y;
};

typedef struct move_structure move;
long long int call_count;
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
//all else are pawns
//from 


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
map<llu,float> min_play_memo;
map<llu,float> max_play_memo;
map<llu,float> evaluate_board_memo;

llu hash_pair(llu,llu);

int min_play_calls, max_play_calls,evaluate_board_calls;

// all else are pawns 

inline float piece_priority(int piece)
{
	switch(piece){
	case KING:  
	case OKING: return 10;
	
	case QUEEN: 	
	case OQUEEN: return 9;

	case BISHOP1: 
	case BISHOP2: return 7;

	case OBISHOP1: 
	case OBISHOP2: return 5;

	case KNIGHT1:  return 3;
	case KNIGHT2:  return 3;
	case OKNIGHT1: return 3;
	case OKNIGHT2: return 3;

	case ROOK1:  return 3;
	case ROOK2:  return 3;
	case OROOK1: return 3;
	case OROOK2: return 3;

	}

	for(int i=PAWN1; i<=PAWN8; i++)
		if( piece == i )	return 1;

	for(int i=OPAWN1; i<= OPAWN8; i++)
		if( piece == i )	return 1;


	return 0;



}


move alpha_beta(vector<llu> &, int,int );
float alpha_beta_min(vector<llu> & , int,float,float  ,int);
float alpha_beta_max(vector<llu> & , int,float,float ,int);


float min_play(vector<llu>,int,int);
float max_play(vector<llu>,int,int);
float evaluate_board(vector<llu> & , int);
llu set_bit(int,int);
llu find_friend_occupied_area(vector<llu> & ,int);
llu find_enemy_occupied_area(vector<llu> &,int);
llu moves_bishop(vector<llu> &,llu);
llu moves_rook(vector<llu> &,llu);
llu moves_king(llu);
llu moves_knight(llu);
llu moves_queen(vector<llu> &,llu);
llu moves_wrapper(vector<llu> &,int);
llu moves_wrapper_2(vector<llu> & ,int);
llu pawn_moves_wrapper(vector<llu> &,int);
llu return_llu();
llu return_one();
inline llu hasher(vector<llu> &);
vector<move> get_all_moves(vector<llu> &,int);
vector<llu> generate_board(vector<llu> &,move);
// taking the move vector as 16 element vector, which have bits on' wherever a chance of move is there from current move
// true 
// army should be the position of the king



vector<llu> find_moves(vector<llu> & board, int army_king )
{
	vector<llu>  moves(16,return_llu());

	for(int i =0; i<16; i++)
		moves[i] = moves_wrapper(board,army_king+i);

	return moves;
}



bool if_piece_under_attack(vector<llu> &  board,int piece){


        llu enemy_attack_area = 0;

        for(int i=(piece<OKING?OKING:KING) ; i<=(piece<OKING?OPAWN8:PAWN8) ; i++)
                enemy_attack_area |= moves_wrapper(board,i);

        if( enemy_attack_area & board[piece] )
                return true;
        else return false;

}


// if the king is under checkmate
bool in_check(vector<llu> & board,int king)
{
	return if_piece_under_attack( board, king);
}


bool in_checkmate(vector<llu> & board, int king)
{
	if ( !in_check(board,king)) return false;

	vector<move> moves = get_all_moves(board,king);

	for(int i =0 ; i< moves.size(); i++)
	{
		vector<llu> temp_board = generate_board(board,moves[i]);
		if( !in_check(temp_board,king) )
			return false;
	}


	return true; 
}


llu set_bit(int x,int y)
{
	if(  y >=0 and y <=7 and x >=0 and x <=7 )
		return ( return_llu() | (return_one())<<(8*(y)+(x)));
	else
		return return_llu();

}


// I don't know how to make zero llu which I was needing for type conversion... so I amde a fucntion
llu return_llu()
{
	llu x =0;
	return x;
} 


// I don't know how to create a constant 1 which is llu so I made a function
llu return_one()
{
	llu x = 1;
	return x;
}
// I am only considering 8X8 board, and I won't write any fucntion only going to use llu as data type
// furthermore I have not considered any rule of chess now. Just the movements I am defining for different pieces
// evey llu passwd to the moves_something function represetns the position of one piece only and
// in return it gets 1-bit on wherever the piece can move 

int find_pos(llu x)
{
	int i  =0;
	for(int i = 0; i< 64; i++)
		if( ((x>>i) & 1) == 1 )
			return i;

	return -1;
}

void print_bitboard(llu x)
{
	int i = 0 ;

	for(int i =0; i<8; i++,printf("\n"))
		for(int j =0; j<8; j++)
			printf("%c",(char)('0' + ((x>>(i*8+j)) & 1)) );

	printf("\n");
}


llu moves_wrapper(vector<llu> & b,int piece )
{
	return (~find_friend_occupied_area(b,piece)) & moves_wrapper_2(b,piece);

}


llu moves_wrapper_2(vector<llu> & b,int piece)
{


	switch(piece){
	case KING:  return moves_king(b[KING]);
	case OKING: return moves_king(b[OKING]);
	
	case QUEEN:  return moves_queen(b,b[QUEEN]);
	case OQUEEN: return moves_queen(b,b[OQUEEN]);

	case BISHOP1: return moves_bishop(b,b[BISHOP1]);
	case BISHOP2: return moves_bishop(b,b[BISHOP2]);

	case OBISHOP1: return moves_bishop(b,b[OBISHOP1]);
	case OBISHOP2: return moves_bishop(b,b[OBISHOP2]);

	case KNIGHT1:  return moves_knight(b[KNIGHT1]);
	case KNIGHT2:  return moves_knight(b[KNIGHT2]);
	case OKNIGHT1: return moves_knight(b[OKNIGHT1]);
	case OKNIGHT2: return moves_knight(b[OKNIGHT2]);

	case ROOK1:  return moves_rook(b,b[ROOK1]);
	case ROOK2:  return moves_rook(b,b[ROOK2]);
	case OROOK1: return moves_rook(b,b[OROOK1]);
	case OROOK2: return moves_rook(b,b[OROOK2]);

	}

	for(int i=PAWN1; i<=PAWN8; i++)
		if( piece == i )	return pawn_moves_wrapper(b,i);

	for(int i=OPAWN1; i<= OPAWN8; i++)
		if( piece == i )	return pawn_moves_wrapper(b,i);


	assert(false);

}



llu moves_king(llu b)
{
	int p  =find_pos(b);


	if ( p < 0 ) return return_llu();
	int x = p%8;
	int y = p/8;


	llu res = 0;

	for ( int i =-1; i<=+1; i++)
		for(int j =-1; j<=+1; j++)
			if( not ( i==j and i ==0 ) )
				res |= set_bit(x+i,y+j);

	return res;

}


llu moves_queen(vector<llu> & board,llu b)
{
	return moves_bishop(board,b) | moves_rook(board,b);
}




llu moves_bishop(vector<llu> & board,llu b)
{
	int p = find_pos(b);
	int x = p%8;
	int y = p/8;
	//if ( p < 0 ) return return_llu();
	if ( p < 0 ) return 0LLU;

	llu res = 0;


	for(int i =0; i>=-7; i--){
		if( not ( i == 0) )
		{
			if( set_bit(x+i,y+i) & (find_friend_occupied_area(board,b)) ) break;
			res |= set_bit(x+i,y+i);
			if( set_bit(x+i,y+i) & (find_enemy_occupied_area(board,b)) ) break;

		}
	}


	for(int i=0; i>=-7; i--){
		if( not ( i == 0) )
		{

			if( set_bit(x+i,y-i) & (find_friend_occupied_area(board,b)) ) break;
			res |= set_bit(x+i,y-i);	
			if( set_bit(x+i,y-i) & (find_enemy_occupied_area(board,b)) ) break;
		}
	}


	for(int i =0; i<=7; i++){
		if( not ( i == 0) )
		{
			if( set_bit(x+i,y+i) & (find_friend_occupied_area(board,b)) ) break;
			res |= set_bit(x+i,y+i);
			if( set_bit(x+i,y+i) & (find_enemy_occupied_area(board,b)) ) break;

		}
	}


	for(int i=0; i<=7; i++){
		if( not ( i == 0) )
		{

			if( set_bit(x+i,y-i) & (find_friend_occupied_area(board,b)) ) break;
			res |= set_bit(x+i,y-i);	
			if( set_bit(x+i,y-i) & (find_enemy_occupied_area(board,b)) ) break;
		}
	}


	return res;
}


llu moves_knight(llu b)
{
	int p = find_pos(b);
	int x =p%8;
	int y =p/8;
	if ( p < 0 ) return return_llu();


	llu res = 0;

	for(int i=-2; i<=2; i+=2 )
		for(int j=-1; j<=1; j++){
			if( not ( j==0 or  i ==0  ) )
				res |= set_bit(x+j,y+i); // y+i , x+j
			if( not ( j==0 or  i ==0  ) )
				res |= set_bit(x+i,y+j); // x+i, y+j
		}

	return res;
}


llu moves_rook(vector<llu> & board, llu b)
{
	int p =  find_pos(b);
	int x = p%8;
	int y = p/8;
	if ( p < 0 ) return return_llu();


	llu res = 0;
/*
	for(int i =-7; i<=7;i++){
		if( not (i ==0 ))
			res |= set_bit(x+i,y);// x+i,y
		if( not (i ==0 ))
			res |= set_bit(x,y+i);
	}
*/

	for(int i =0; i>=-7; i--){
		if( not ( i == 0) )
		{
			if( set_bit(x+i,y) & (find_friend_occupied_area(board,b)) ) break;
			res |= set_bit(x+i,y);
			if( set_bit(x+i,y) & (find_enemy_occupied_area(board,b)) ) break;

		}
	}


	for(int i=0; i>=-7; i--){
		if( not ( i == 0) )
		{

			if( set_bit(x,y+i) & (find_friend_occupied_area(board,b)) ) break;
			res |= set_bit(x,y+i);	
			if( set_bit(x,y+i) & (find_enemy_occupied_area(board,b)) ) break;
		}
	}


	for(int i =0; i<=7; i++){
		if( not ( i == 0) )
		{
			if( set_bit(x+i,y) & (find_friend_occupied_area(board,b)) ) break;
			res |= set_bit(x+i,y);
			if( set_bit(x+i,y) & (find_enemy_occupied_area(board,b)) ) break;

		}
	}


	for(int i=0; i<=7; i++){
		if( not ( i == 0) )
		{

			if( set_bit(x,y+i) & (find_friend_occupied_area(board,b)) ) break;
			res |= set_bit(x,y+i);	
			if( set_bit(x,y+i) & (find_enemy_occupied_area(board,b)) ) break;
		}
	}





	return res;

}

// dir == true /false for different type of pawn
llu moves_pawn(llu b,bool dir,bool attack)
{
	int p = find_pos(b);
	int x = p%8;
	int y = p/8;
	if ( p < 0 ) return return_llu();


	llu res = 0;

	if ( dir )
	{
		if( y+1 >= 0 and y+1 <=7 ) 
		{
			if( not attack ) res |= set_bit(x,y+1);
			if(attack )
				res |= set_bit(x-1,y+1);
			if(attack )
				res |= set_bit(x+1,y+1);
		}

	}
	else {
		if( y-1 >=0 and y-1 <= 7 )
		{
			if ( not attack ) res |= set_bit(x,y-1);
			if( attack )
				res |= set_bit(x-1,y-1);
			if( attack)
				res |= set_bit(x+1,y-1);
		}
	}

	return res;

}


llu find_enemy_occupied_area(vector<llu> & board,int piece)
{
        llu occupied_enemy_area = 0;

        for(int i=( piece<OKING? OKING : KING );   i <= ( piece < OKING? OPAWN8 : PAWN8 ); i++)
                occupied_enemy_area |= board[i];

        return occupied_enemy_area;
}



llu find_friend_occupied_area(vector<llu> & board,int piece)
{
        llu occupied_friend_area = 0;

        for(int i=( piece<OKING? KING : OKING );   i <= ( piece < OKING? PAWN8 : OPAWN8 ); i++)
                occupied_friend_area |= board[i];

        return occupied_friend_area;
}





llu pawn_moves_wrapper(vector<llu> & board,int pawn)
{
        llu pawn_attack_board = moves_pawn(board[pawn],pawn<OKING?true:false,true);

        llu  occupied_enemy_area = find_enemy_occupied_area(board,pawn);
	llu  occupied_friend_area = find_friend_occupied_area(board,pawn);

        pawn_attack_board = ( occupied_enemy_area & pawn_attack_board ) ;               
	

	llu pawn_move_board = (  moves_pawn(board[pawn], pawn<OKING?true:false,false) & ( ~occupied_friend_area & ~occupied_enemy_area ) );



	return pawn_attack_board | pawn_move_board;
 
}



void print_vec_bitboard(vector<llu> v)
{
	for(int i =0; i< v.size(); i++)
		print_bitboard(v[i]);
	cout << endl;
}


void print_move_vector(vector< move> v )
{
	for(int i =0; i< v.size(); i++)
		cout << v[i].piece << " " <<v[i].x << " "<< v[i].y << " , ";
	cout << endl;
}


vector<move> get_move_vector(llu b,int piece)
{
	vector< move> v;

	for(int y=0; y <8; y++)
		for(int x=0; x<8; x++)
			if( ( b >> ( 8*y+x)) & 1 )
				v.push_back((move){piece,x,y});


	return v;


}


vector<move> get_all_moves(vector<llu> & board , int army_king)
{
	vector<move> ret_v;

	
	vector<llu>  moves_bit = find_moves(board,army_king);

	for(int i=0; i<16; i++) {
		vector<move> moves_list =  get_move_vector(moves_bit[i],i+army_king);
		ret_v.insert(ret_v.end(), moves_list.begin(), moves_list.end() );
	}

//	cout << "Army :" << army_king << endl;
	
//	print_move_vector(ret_v);	
//	cout << endl;
	return ret_v;

}




vector<llu> generate_board(vector<llu> & board,move m ){

	vector<llu> new_board(board);

	for(int i=(m.piece<OKING?OKING:KING); i< ((m.piece<OKING)? OPAWN8:PAWN8); i++)
		if( m.x == find_pos(new_board[i])%8 and m.y == find_pos(new_board[i])/8 ){
			new_board[i] = 0;
			break;
		}

	new_board[m.piece] = set_bit( m.x,m.y);	

	return new_board;
}
		

	

	
move minimax(vector<llu> board,int army_king,int depth)
{
	
	vector<move> moves_list = get_all_moves(board,army_king);
	
	//TODO take care of this -1,0,0 return value
	if( moves_list.size() == 0 or depth == 0){
	//	cout << "minimax, no moves to play"<<endl;
		return  (move){-1,0,0};
	}

	move best_move = moves_list[0];
	float best_score = -99999;

	for(int i=0; i< moves_list.size(); i++){
		vector<llu> clone_board = generate_board(board,moves_list[i]);
		float score = min_play(clone_board,army_king<OKING?OKING:KING,depth);
		
		if( score  > best_score){
			best_move = moves_list[i];
			best_score = score;
		}
	}


	return best_move;
}

bool game_over(vector<llu> board)
{
	if( in_checkmate(board,KING) || in_checkmate(board,OKING))
		return true;

	return false;

}


float evaluate_board(vector<llu> & board,int army_king)
{

	//cout << evaluate_board_memo.size() << " " << ++evaluate_board_calls << "\n";
	
	

	llu board_hash = hash_pair(hasher(board),army_king) ;

	if( evaluate_board_memo.find(board_hash) != evaluate_board_memo.end() )
		return evaluate_board_memo[board_hash];
	else{ 
	

	if ( in_checkmate(board,army_king) or in_check(board,army_king) ) { return evaluate_board_memo[board_hash] =(float)-99999;}
	if ( in_checkmate(board,army_king<OKING?OKING:KING) or in_check(board,army_king<OKING?OKING:KING)) { return evaluate_board_memo[board_hash] =(float)99999;}

		
	
	float sum = 0.0;

	for(int i =KING; i<OKING; i++)
		sum += (  (board[i]!=return_llu()) - (board[i+OKING]!=return_llu()) ) *piece_priority(i);

	

	if( army_king == KING)
	{
		
		return evaluate_board_memo[board_hash] = sum;
	}
	else
	{
	
		return evaluate_board_memo[board_hash] = sum;
	}

	}

}

	
float min_play(vector<llu> board,int army_king,int depth)
{
	//cout << "minplay: " << min_play_memo.size() << " " << (++min_play_calls)<<endl;
	
	if ( game_over(board) or depth <= 0 )
		return evaluate_board(board,army_king);


	llu board_hash = hasher(board);

	if( min_play_memo.find(board_hash) != min_play_memo.end() )
		return min_play_memo[board_hash];
	else {
	vector<move> moves_list = get_all_moves(board,army_king);

	if( moves_list.size() == 0 ) return evaluate_board(board,army_king);

	float best_score = 99999;

	for(int i =0; i<moves_list.size(); i++){
		vector<llu> clone_board = generate_board(board,moves_list[i]);
		float score = max_play(clone_board,army_king<OKING?OKING:KING,depth-1);
	
		if(score < best_score )
			best_score = score;	
	}

	return min_play_memo[board_hash] = best_score;

	}
}


float max_play(vector<llu> board,int army_king,int depth)
{
	//cout << "maxplay: " << max_play_memo.size() << " " << (++max_play_calls) << endl;
	if ( game_over(board) or depth <= 0 )
		return evaluate_board(board,army_king);

	llu board_hash = hasher(board);

	if( max_play_memo.find(board_hash) != max_play_memo.end() )
		return max_play_memo[board_hash];
	else {
	vector<move> moves_list = get_all_moves(board,army_king);

	if( moves_list.size() == 0 ) return evaluate_board(board,army_king);

	float best_score = -99999;

	for(int i=0; i<moves_list.size(); i++){
		vector<llu> clone_board = generate_board(board,moves_list[i] );
		float score = min_play(clone_board,army_king<OKING?OKING:KING, depth-1);

		if(score > best_score )
			best_score = score;
	}


	return max_play_memo[board_hash] = best_score;
	}
}


	
void pretty_print_board(vector<llu> board)
{
	vector<int> temp(64,0);

	for(int i =0; i<32; i++)
	{
		int x =find_pos(board[i])%8,y = find_pos(board[i])/8;
		temp[y*8+x] = i;
	}

	for(int i=0; i<8; i++,putchar('\n'))
		for(int j=0; j<8; j++,putchar(' '))
			cout << temp[i*8+j];	


}


  
inline llu hasher(vector<llu> & v )
{
	llu hash = 0;

	for(int i= 0; i<v.size(); i++)
		hash = v[i] + 0x9e3779b9 + (hash<<6) + ( hash>>2);

	return hash;
	
}

inline llu hash_pair(llu a,llu b)
{
	vector<llu> v;
	v.push_back(a);v.push_back(b);
	return hasher(v);
}


move alpha_beta(vector<llu> & board,int army_king,int depth)
{
	if( depth <=0 or game_over(board) )	return (move){-1,0,0};

	vector<move> moves_list = get_all_moves(board,army_king);

	if( moves_list.size() == 0 ) return (move){-1,0,0};


	float best_score = -99999;

	float alpha =-99999, beta = 99999;
	move best_move = moves_list[0];
	


	for(int i=0; i<moves_list.size(); i++){
		vector<llu> clone_board = generate_board(board,moves_list[i] );
		float score = alpha_beta_min(clone_board,army_king<OKING?OKING:KING, alpha,beta,depth-1);

		if(score < best_score ){
			best_move = moves_list[i];
			best_score = score;
		}
	}
	//cout << "best_score" << " "<< best_score << endl;
	return best_move;
}
	
float alpha_beta_min(vector<llu> & board,int army_king, float alpha, float beta, int depth )
{
	if( depth ==0 or game_over(board) ) return evaluate_board(board,army_king);

	llu board_hash = hasher(board);

	if( min_play_memo.find(board_hash) != min_play_memo.end() )
		return min_play_memo[board_hash];
	else {
	vector<move> moves_list = get_all_moves(board,army_king);

	if( moves_list.size() == 0 ) return evaluate_board(board,army_king);


	float _alpha=alpha;
	float _beta =beta;

	for(int i =0; i<moves_list.size(); i++){
		vector<llu> clone_board = generate_board(board,moves_list[i]);
		float score = alpha_beta_max(clone_board,army_king<OKING?OKING:KING,_alpha,_beta,depth-1);

		if( score <= _alpha)
			return min_play_memo[board_hash] = _alpha;
		
		if( score < beta)
			_beta = score;
		
	
		
	}

	return min_play_memo[board_hash] = _beta;

	}

}

	
float alpha_beta_max(vector<llu> & board,int army_king, float alpha, float beta, int depth )
{
	if( depth ==0 or game_over(board) ) return evaluate_board(board,army_king);

	llu board_hash = hasher(board);

	if( min_play_memo.find(board_hash) != min_play_memo.end() )
		return min_play_memo[board_hash];
	else {
	vector<move> moves_list = get_all_moves(board,army_king);

	if( moves_list.size() == 0 ) return evaluate_board(board,army_king);


	float _alpha = alpha;
	float _beta = beta;

	for(int i =0; i<moves_list.size(); i++){
		vector<llu> clone_board = generate_board(board,moves_list[i]);
		float score = alpha_beta_min(clone_board,army_king<OKING?OKING:KING,_alpha,_beta,depth-1);
	
		if( score >= _beta)
			return _beta;
		if( score > _alpha )
			_alpha =score;
	

		
	}

	return max_play_memo[board_hash] = _alpha;

	}

}



int main(int argc,char *argv[])
{

	vector<llu> bb(32,0);


	int army_king = atoi(argv[1]);
	int depth     = atoi(argv[2]);


	for(int i =0; i<32; i++)
	{
		int x,y;
		cin >> y >> x;
		--x,--y;
		if( x > -1 and y >-1)
			bb[i] = set_bit(x,y);
		else
			bb[i] = return_llu();
	//	cout << "piece : " << i << endl;
	//	print_bitboard(bb[i]);
	}


	//pretty_print_board(bb);	


	move ans = alpha_beta(bb,army_king,depth);
	
	cout << ans.piece << " " << ans.x <<" "<< ans.y << endl;

	//if(  ans.piece != -1 )	pretty_print_board(generate_board(bb,ans));	
	
	return 0;

}
