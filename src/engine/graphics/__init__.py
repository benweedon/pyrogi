from operator import attrgetter
import engine
from engine.util.vector import Vec2

class Graphics(object):
    def init_window(self, window_dimensions, tile_dimensions, caption):
        raise NotImplementedError()
    def clear_screen(self):
        raise NotImplementedError()
    def draw_tile(self, character, fg_color, bg_color):
        raise NotImplementedError()


class Tile(object):
    def __init__(self, character, fg_color, bg_color):
        self.character = character
        self.fg_color = fg_color
        self.bg_color = bg_color
    
    def draw(self, g, position):
        g.draw_tile(position, self.character, self.fg_color, self.bg_color)


class Color(object):
    def __init__(self, r, g, b, a=255):
        self.r = r
        self.g = g
        self.b = b
        self.a = a
    
    def to_RGB_tuple(self):
        return (self.r, self.g, self.b)
    def to_RGBA_tuple(self):
        return (self.r, self.g, self.b, self.a)
    
    def __hash__(self):
        return hash(self.to_RGBA_tuple())
    def __eq__(self, other):
        return self.r == other.r and self.g == other.g and self.b == other.b and self.a == other.a

class Paint(object):
    def get_tile_color(self, absolute_position, relative_position):
        """absolute_position is absolute in the window, relative_position is relative_position to the Drawable being colored"""
        raise NotImplementedError()
    def tick(self, millis):
        pass
class SolidPaint(Paint):
    def __init__(self, color):
        self.color = color
    def get_tile_color(self, absolute_position, relative_position):
        return self.color


class Drawable(object):
    def __init__(self, position, fg_paint=None, bg_paint=None):
        self.position = position
        self.fg_paint = fg_paint
        self.bg_paint = bg_paint
        self.tiles = []
    
    def add_tile(self, tile, offset):
        self.tiles.append((tile, offset))
        # sort in top-to-bottom, left-to-right text order
        self.tiles.sort(key=lambda pair: attrgetter('y', 'x')(pair[1]))
    def add_rectangle(self, dimensions, character, fg_color, bg_color):
        for x in xrange(dimensions.x):
            for y in xrange(dimensions.y):
                self.add_tile(Tile(character, fg_color, bg_color), Vec2(x, y))
    
    def update_drawable(self, millis):
        self._update_paint(millis, self.fg_paint, True)
        self._update_paint(millis, self.bg_paint, False)
    
    def _update_paint(self, millis, paint, is_foreground):
        if paint is not None:
            paint.tick(millis)
            for tile, offset in self.tiles:
                color = paint.get_tile_color(self.position+offset, offset)
                if is_foreground:
                    tile.fg_color = color
                else:
                    tile.bg_color = color
    
    def draw(self, g):
        for tile, offset in self.tiles:
            tile.draw(g, self.position+offset)
    
    def contains_position(self, position):
        for tile, offset in self.tiles:
            tile_position = self.position + offset
            if tile_position == position:
                return True
        return False
    
    def write_text(self, text):
        characters = engine.parse_text_into_characters(text)
        for tile, offset in self.tiles:
            if len(characters) == 0:
                break
            tile.character = characters[0]
            characters.pop(0)