#include<bits/stdc++.h>

using namespace std;


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

// all else are pawns 


llu set_bit(int,int);

llu moves_bishop(llu);
llu moves_rook(llu);
llu moves_king(llu);
llu moves_queen(llu);
llu moves_wrapper(llu,int);
llu return_llu();
llu return_one();

// taking the move vector as 16 element vector, which have bits on' wherever a chance of move is there from current move
// true 
// army should be the position of the king





vector<llu> find_moves(vector<llu> & board, int army_king )
{
	vector<llu> moves(16,return_llu());

	for(int i =0; i<16; i++)
	{
		moves[i] = moves_wrapper(board,army_king+i);
	}


	return moves;

}






bool if_piece_under_attack(vector<llu> &  board,int piece){


        llu enemy_attack_area = 0;

        for(int i=(piece<OKING?OKING:KING) ; i<=(piece<OKING?OPAWN8:PAWN8) ; i++)
                enemy_attack_area |= board[i];

        if( enemy_attack_area & board[piece] )
                return true;
        else return false;

}


// if the king is under checkmate
bool check_mate(vector<llu> & board,int army_king)
{
	return if_piece_under_attack( board, army_king);
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
}

void print_bitboard(llu x)
{
	int i = 0 ;

	for(int i =0; i<8; i++,printf("\n"))
		for(int j =0; j<8; j++)
			printf("%c",(char)('0' + ((x>>(i*8+j)) & 1)) );

	printf("\n");
}


llu moves_wrapper(vector<llu> b,int piece)
{
	switch(piece){
	case KING:  return moves_king(b[KING]);
	case OKING: return moves_king(b[OKING]);
	
	case QUEEN:  return moves_queen(b[QUEEN]);
	case OQUEEN: return moves_queen(b[OQUEEN]);

	case BISHOP1: return moves_bishop(b[BISHOP1]);
	case BISHOP2: return moves_bishop(b[BISHOP2]);

	case OBISHOP1: return moves_bishop(b[OBISHOP1]);
	case OBISHOP2: return moves_bishop(b[OBISHOP2]);

	case KNIGHT1:  return moves_knight(b[KNIGHT1]);
	case KNIGHT2:  return moves_knight(b[KNIGHT2]);
	case OKNIGHT1: return moves_knight(b[OKNIGHT1]);
	case OKNIGHT2: return moves_knight(b[OKNIGHT2]);

	case ROOK1:  return moves_rook(b[ROOK1]);
	case ROOK2:  return moves_rook(b[ROOK2]);
	case OROOK1: return moves_rook(b[OROOK1]);
	case OROOK2: return moves_rook(b[OROOK2]);

	}

	for(int i=PAWN1; i<=PAWN8; i++)
		if( piece == i )	return pawn_moves_wrapper(b[i]);

	for(int i=OPAWN1; i<= OPAWN8; i++)
		if( piece == i )	return pawn_moves_wrapper(b[i]);


	exit(-1);

}



llu moves_king(llu b)
{
	int p  =find_pos(b);
	int x = p%8;
	int y = p/8;


	llu res = 0;

	for ( int i =-1; i<=+1; i++)
		for(int j =-1; j<=+1; j++)
			if( not ( i==j and i ==0 ) )
				res |= set_bit(x+i,y+j);

	return res;

}


llu moves_queen(llu b)
{
	return moves_bishop(b) | moves_rook(b);
}




llu moves_bishop(llu b)
{
	int p = find_pos(b);
	int x = p%8;
	int y = p/8;

	cout << x << " " << y << endl;

	llu res = 0;


	for(int i =-7; i<=7; i++){
		if( not ( i == 0) )
			res |= set_bit(x+i,y+i);
		if( not ( i == 0) )
			res |= set_bit(x+i,y-i);
	}

	return res;
}


llu moves_knight(llu b)
{
	int p = find_pos(b);
	int x =p%8;
	int y =p/8;

	cout << x << " "<< y << endl;

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


llu moves_rook(llu b)
{
	int p =  find_pos(b);
	int x = p%8;
	int y = p/8;

	cout << x << " " << y << endl;

	llu res = 0;

	for(int i =-7; i<=7;i++){
		if( not (i ==0 ))
			res |= set_bit(x+i,y);// x+i,y
		if( not (i ==0 ))
			res |= set_bit(x,y+i);
	}

	return res;

}

// dir == true /false for different type of pawn
llu moves_pawn(llu b,bool dir,bool attack)
{
	int p = find_pos(b);
	int x = p%8;
	int y = p/8;


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

        for(int i=( piece>OKING? OKING : KING );   i <= ( piece > OKING? OPAWN8 : PAWN8 ); i++)
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





int main()
{

	vector<llu> bb(32,0);

	

	for(int i =0; i< 64 ;i++)
	{
		bb[OPAWN1] = return_one()<<i;	
		cout << "i = " << i << endl;
		print_bitboard(return_one()<<i);	
		print_bitboard(pawn_moves_wrapper(bb,OPAWN1));
		system("sleep 0.1");
	
	}

}
