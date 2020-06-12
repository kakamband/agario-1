
from typing import Any, Dict

from frost.ext import Cog
from frost.server import auth_required, logger, Memory
from frost.server.database import managed_session

from server.headers import Status


class Agario(Cog, route='agario'):
    players = dict()

    @auth_required
    def join(
        data: Dict[str, Any],
        token: str,
        id_: str,
        **kwargs: Any
    ) -> None:
        user = Memory.logged_in_users[id_]

        Agario.players[id_] = {
            'object': user,
            'score': 0
        }

        kwargs['client_send']({
            'headers': {
                'path': 'agario/post_join',
                'status': Status.SUCCESS.value
            }
        })

        logger.info(f'{user.username} joined the game.')

    @auth_required
    def leave(
        data: Dict[str, Any],
        token: str,
        id_: str,
        **kwargs: Any
    ) -> None:
        try:
            Agario.players.pop(id_)

        except KeyError:
            pass

        finally:
            kwargs['client_send']({
                'headers': {
                    'path': 'agario/post_leave',
                    'status': Status.SUCCESS.value
                }
            })

    @auth_required
    def send_pos(
        data: Dict[str, Any],
        token: str,
        id_: str,
        **kwargs: Any
    ) -> None:
        user = Agario.players.get(id_)

        if user is None:
            return

        user.pos = data['pos']

        for player in Agario.players.values():
            if player.id == id_:
                continue

            kwargs['send'](player.conn, {
                'headers': {
                    'path': 'agario/send_pos'
                },
                'id': id_,
                'pos': data['pos']
            })
