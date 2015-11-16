def alphaBetaMin(board,color,alpha,beta, depth):
        if depth == 0 or helper.game_over(board, color) :
                return evaluate_board(board,color)

        moves_list = helper.get_moves(board,color)

        for move in moves_list:
                clone_board = helper.generate_board(board,move)         

                score = alphaBetaMax(clone_board,opposite_army[color],alpha,beta,depth-1)
                if score <= beta:
                        return alpha
                if score < alpha:
                        beta = score

        return beta

def alphaBetaMax(board,color,alpha,beta, depth):
        if depth == 0 or helper.game_over(board, color) :
                return evaluate_board(board,color)

        moves_list = helper.get_moves(board,color)

        for move in moves_list:
                clone_board = helper.generate_board(board,move)

                score = alphaBetaMin(clone_board,opposite_army[color],alpha,beta,depth-1)
                if score >= beta:
                        return beta
                if score > alpha:
                        alpha = score

        return alpha

