from django.shortcuts import render
from game.game3x3.Moves import Move
from game.models import GameState
from django.core.exceptions import ObjectDoesNotExist


def game_action(request, action: int):

	"""
	Возвращает страницу игры с измененным относительно предыдущего хода состоянием.
	Принимает на вход параметр :action: int определяющий следующий ход.
	1 = лево
	2 = право
	3 = вверх
	4 = низ
	5 = начать игру заново
	"""

	if not request.session.session_key:
		request.session.create()

	try:
		game_state = GameState.objects.get(session_key=request.session.session_key)
		object_exists = True
	except ObjectDoesNotExist:
		object_exists = False

	if object_exists:
		move = Move()

		move.pattern = [
			[game_state.cell1, game_state.cell2, game_state.cell3],
			[game_state.cell4, game_state.cell5, game_state.cell6],
			[game_state.cell7, game_state.cell8, game_state.cell9]
		]

		if action == 1:
			move.action_left()
		elif action == 2:
			move.action_right()
		elif action == 3:
			move.action_up()
		elif action == 4:
			move.action_down()
		elif action == 5:
			move.pattern = [
				[0, 0, 0],
				[0, 0, 0],
				[0, 0, 0]
			]
			move.generate_tile_on_move()
			move.generate_tile_on_move()

		game_state.cell1 = move.pattern[0][0]
		game_state.cell2 = move.pattern[0][1]
		game_state.cell3 = move.pattern[0][2]
		game_state.cell4 = move.pattern[1][0]
		game_state.cell5 = move.pattern[1][1]
		game_state.cell6 = move.pattern[1][2]
		game_state.cell7 = move.pattern[2][0]
		game_state.cell8 = move.pattern[2][1]
		game_state.cell9 = move.pattern[2][2]

		game_state.save()

	else:
		return render(request,
		              'game/game_error.html')

	context = {
		'cell1': move.pattern[0][0],
		'cell2': move.pattern[0][1],
		'cell3': move.pattern[0][2],
		'cell4': move.pattern[1][0],
		'cell5': move.pattern[1][1],
		'cell6': move.pattern[1][2],
		'cell7': move.pattern[2][0],
		'cell8': move.pattern[2][1],
		'cell9': move.pattern[2][2]
	}
	return render(request,
	              'game/game.html',
	              context=context)


def game_index(request):
	"""
	Стартовая страница игры (без идентификатора действия передаваемого в url)
	"""

	if not request.session.session_key:
		request.session.create()

	try:
		game_state = GameState.objects.get(session_key=request.session.session_key)
		object_exists = True
	except ObjectDoesNotExist:
		object_exists = False

	if object_exists:
		move = Move()

		move.pattern = [
			[game_state.cell1, game_state.cell2, game_state.cell3],
			[game_state.cell4, game_state.cell5, game_state.cell6],
			[game_state.cell7, game_state.cell8, game_state.cell9]
		]
		print(move)
	else:
		game_state = GameState.objects.create(session_key=request.session.session_key)
		move = Move()
		print(move)
		game_state.cell1 = move.pattern[0][0]
		game_state.cell2 = move.pattern[0][1]
		game_state.cell3 = move.pattern[0][2]
		game_state.cell4 = move.pattern[1][0]
		game_state.cell5 = move.pattern[1][1]
		game_state.cell6 = move.pattern[1][2]
		game_state.cell7 = move.pattern[2][0]
		game_state.cell8 = move.pattern[2][1]
		game_state.cell9 = move.pattern[2][2]

		game_state.save()

	context = {
		'cell1': move.pattern[0][0],
		'cell2': move.pattern[0][1],
		'cell3': move.pattern[0][2],
		'cell4': move.pattern[1][0],
		'cell5': move.pattern[1][1],
		'cell6': move.pattern[1][2],
		'cell7': move.pattern[2][0],
		'cell8': move.pattern[2][1],
		'cell9': move.pattern[2][2],
	}

	return render(request,
	              'game/game.html',
	              context=context)
