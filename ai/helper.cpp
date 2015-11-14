


#define llu long long unsigned int
#define KING    0
#define QUEEN   1
#define BISHOP1 2
#define KNIGHT1 4
#define ROOK1   6
#define PAWN1   8
#define PAWN8  15
//all else are pawns
//from 


#define OKING   16
#define OQUEEN  17
#define OBISHOP 18
#define OKNIGHT 20
#define OROOK   22
#define OPAWN1  24
#define OPAWN8  31

// all else are pawns 

llu pawn_moves_wrapper(vector<llu> & board,int pawn)
{
	pawn_attack_board = moves_pawn(board[pawn],pawn<OKING?true:false,true);

	llu  occupied_enemy_area =0 ;

	for(int i=(pawn<OKING?OKING:KING) ; i<=(pawn<OKING?OPAWN8:PAWN8) ; i++)
		enemy_occupied_area |= board[i];

	pawn_attack_board = ( occupied_enemy_area & pawn_attack_board )	;

	

		
}





bool if_piece_under_attack(vector<llu> &  board,int piece){
{

	llu enemy_attack_area = 0;

	for(int i=(piece<OKING?OKING:KING) ; i<=(piece<OKING?OPAWN8:PAWN8) ; i++)
		enemy_attack_area |= board[i];		
		
	if( enemy_attack_area & board[piece] )
		return true;
	else return false;

}
