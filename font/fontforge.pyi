from typing import Iterator, Optional

# a minimal set of FontForge API for type hinting

__version__: str

def activeFont() -> Optional[Font]:
    """
    Returns the currently open font, or None if no font is open.
    This is useful for working with a font without knowing its name or location.

    Returns:
        Optional[Font]: The currently active Font object, or None if no font is active.
    """
    ...

def open(path: str) -> Font:
    """
    Opens a font file at the specified path and returns a Font object representing the font.
    
    Args:
        path (str): The path to the font file.
        
    Returns:
        Font: A Font object representing the opened font.
    """
    ...

def unicodeFromName(glyph_name: str) -> int:
    """
    Converts a glyph name to its corresponding Unicode codepoint, if any.

    Args:
        glyph_name (str): The name of the glyph.
        
    Returns:
        int: The Unicode codepoint corresponding to the glyph name, or -1 if no mapping exists.
    """
    ...

def version() -> str:
    """
    Returns the version of FontForge as a string.

    Returns:
        str: The version of FontForge.
    """
    ...

class Font:
    """
    Represents a font, allowing access to its glyphs and various font properties.

    """

    path: Optional[str]
    """
    The file path of the font, or None if the font has not been saved.
    """
    ascent: int
    """
    The font's ascent (the distance from the baseline to the highest point of any glyph in the font).
    """
    descent: int
    """
    The font's descent (the distance from the baseline to the lowest point of any glyph in the font).
    """
    em: int
    """
    em: The em size of the font. Setting this will scale the entire font to the new size.
    """
    fontname: str
    """
    PostScript font name
    
    Note that in a CID keyed font this will be the name of the current subfont. Use cidfontname for the name of the font as a whole.
    """

    def createChar(self, unicode: int, name: Optional[str] = None) -> "Glyph":
        """
        Create (and return) a character at the specified unicode codepoint in this font and optionally name it. If you wish to create a glyph with no unicode codepoint, set the first argument to -1 and specify a name.

        If there is already a character at that (positive) codepoint then it is returned. If the optional name parameter is included and differs from its current name then the character is also renamed.


        Args:
            unicode (int): The Unicode codepoint for the glyph.
            name (Optional[str]): The name of the glyph.

        Returns:
            Glyph: The created Glyph object.
        """
        ...
    def glyphs(self) -> Iterator[Glyph]:
        """
        Returns an iterator which will return the glyphs in the font. By default they will be returned in “GID” order, but if type is specified as “encoding” they will be returned in encoding order. If returned in encoding order it is possible that a glyph will be returned more than once if there are multiple encoding slots which reference it.
        """

class Glyph:
    """
    Represents a single glyph in a font, including properties such as width and name,
    and methods for transforming and editing the glyph.
    """

    width: int
    """
    The advance width of the glyph. See also Glyph.vwidth
    """
    vwidth: int
    """
    The vertical advance width of the glyph. See also Glyph.width.
    """
    glyphname: str
    """
    The name of the glyph.
    """

    # @overload
    # def addPosSub(
    #     self, 
    #     subtable_name: str, 
    #     variant: str
    # ) -> None:
    #     """
    #     Adds single substitution data to the glyph.
    #     """

    # @overload
    # def addPosSub(
    #     self, 
    #     subtable_name: str, 
    #     variants: Tuple[str]
    # ) -> None:
    #     """
    #     Adds multiple or alternated substitutions data to the glyph.
    #     """

    # @overload
    # def addPosSub(
    #     self, 
    #     subtable_name: str, 
    #     ligature_components: Tuple[str]
    # ) -> None:
    #     """
    #     Adds ligature components data to the glyph.
    #     """

    # @overload
    # def addPosSub(
    #     self, 
    #     subtable_name: str, 
    #     xoff: int, 
    #     yoff: int, 
    #     xadv: int, 
    #     yadv: int
    # ) -> None:
    #     """
    #     Adds single positioning data to the glyph.
    #     """

    # @overload
    # def addPosSub(
    #     self, 
    #     subtable_name: str, 
    #     other_glyph_name: str, 
    #     kerning: int
    # ) -> None:
    #     """
    #     Adds traditional, one-axis kerning data to the glyph.
    #     """

    # @overload
    # def addPosSub(
    #     self, 
    #     subtable_name: str, 
    #     other_glyph_name: str, 
    #     xoff1: int, 
    #     yoff1: int, 
    #     xadv1: int, 
    #     yadv1: int, 
    #     xoff2: int, 
    #     yoff2: int, 
    #     xadv2: int, 
    #     yadv2: int
    # ) -> None:
    #     """
    #     Adds pairwise positionings (kerning) data to the glyph.
    #     """

    def clear(self) -> None:
        """
        With no arguments, clears the contents of the glyph (and marks it as not glyph.isWorthOutputting()). It is not possible to clear the guide layer with this function. layer may be either an integer index or a string. 
        """
        ...

    def importOutlines(self, path: str, scale: bool = True, **kwargs) -> None: # type: ignore
        """
        Uses the file's extension to determine behavior. Imports outline descriptions (eps, svg, glif files) into the foreground layer. Imports image descriptions (bmp, png, xbm, etc.) into the background layer. The following optional keywords modify the import process for various formats:

        Args:
            path (str): The path to the SVG file.
            scale (bool): Scale imported images and SVGs to ascender height.
        """
        ...

    def boundingBox(self) -> tuple[int, int, int, int]:
        """
        Returns a tuple representing a rectangle (xmin,ymin, xmax,ymax) which is the minimum bounding box of the glyph.

        Returns:
            Tuple[int, int, int, int]: The (xmin, ymin, xmax, ymax) of the bounding box.
        """
        ...

    def transform(self, matrix: tuple[float, float, float, float, float, float]) -> None:
        """
        Transforms the glyph by the matrix.

        Args:
            matrix (Tuple[float, float, float, float, float, float]): The transformation matrix (scaleX, skewX, skewY, scaleY, positionX, positionY).
        """
        ...

    def removeOverlap(self) -> None:
        """
        Removes overlapping areas. See also glyph.intersect() and glyph.exclude().
        """
        ...

    def addExtrema(self) -> None:
        """
        Extrema should be marked by on-curve points. If a curve lacks a point at an extrema this command will add one. Flags may be one of the following strings
        """
        ...
