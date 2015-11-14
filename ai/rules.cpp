#include<bits/stdc++.h>

using namespace std;

#define llu long long int


llu moves_bishop(llu);
llu moves_rook(llu);


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


llu moves_king(llu b)
{
	int p  =find_pos(b);
	int x = p%8;
	int y = p/8;

	cout << x << " " << y << endl;

	llu res = 0;

	for ( int i =-1; i<=+1; i++)
		for(int j =-1; j<=+1; j++)
			if( x+i >=0 and x+i <= 7 and y+j >=0 and y+j <=7 and not ( i==j and i ==0 ) )
				res |= ( 1<<(8*(y+j)+(x+i)));

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
		if( x+i >=0 and x+i <=7 and y+i >=0 and y+i <=7 and not ( i == 0) )
			res |= ( return_llu() | (return_one())<<(8*(y+i)+(x+i)));
		if( x+i >=0 and x+i <=7 and y-i >=0 and y-i <=7 and not ( i == 0) )
			res |= ( return_llu() | (return_one())<<(8*(y-i)+(x+i)));
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
			if( not ( j==0 or  i ==0  ) and x+j >=0 and x+j <=7 and y+i <=7 and y+i >=0 )
				res |= (return_llu() | (return_one()) << (8*(y+i)+(x+j)));
			if( not ( j==0 or  i ==0  ) and y+j >=0 and y+j <=7 and x+i <=7 and x+i >=0 )
				res |= (return_llu() | (return_one()) << (8*(y+j)+(x+i)));
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
		if( x+i >= 0 and x+i <= 7 and not (i ==0 ))
			res |= (return_llu() | (return_one())<<(8*(y)+(x+i)));
		if( y+i >= 0 and y+i <= 7 and not (i ==0 ))
			res |= (return_llu() | (return_one())<<(8*(y+i)+(x)));
	}

	return res;

}

// dir == true /false for different type of pawn
llu moves_pawn(llu b,bool dir)
{
	int p = find_pos(b);
	int x = p%8;
	int y = p/8;

	cout << x << " " << y << endl;

	llu res = 0;

	if ( dir )
	{
		if( y+1 >= 0 and y+1 <=7 ) 
		{
			res |= ( return_llu() | (return_one())<<(8*(y+1)+x));
			if( x-1 >=0 and x-1 <=7 )
				res |= (return_llu() | (return_one())<<(8*(y+1)+x-1));
			if( x+1 >=0 and x+1 <=7 )
				res |= (return_llu() | (return_one())<<(8*(y+1)+x+1));
		}

	}
	else {
		if( y-1 >=0 and y-1 <= 7 )
		{
			res |= (return_llu() | (return_one())<<(8*(y-1)+x));
			if( x-1 >=0 and x-1 <=7 )
				res |= (return_llu() | (return_one())<<(8*(y-1)+x-1));
			if( x+1 >=0 and x+1 <=7 )
				res |= (return_llu() | (return_one())<<(8*(y-1)+x+1));
		}
	}

	return res;

}


int main()
{
	for(int i =0; i< 20 ;i++)
	{
		print_bitboard(1<<i);	
		print_bitboard(moves_pawn((1<<i),false));
	}

}
