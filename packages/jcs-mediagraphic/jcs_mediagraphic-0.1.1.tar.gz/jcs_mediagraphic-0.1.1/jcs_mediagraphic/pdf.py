from PIL import Image, ImageChops
from fpdf import FPDF


def thousands_separators(number: int or str or float, separator: str=" ") -> str:
    """Convert a number to a string with thousands separators.
    
    :param number: The number that we would like to convert in string with thousands separators
    :type number: int or string or float

    :param separator: Separator used
    :default separator: space
    :type separator: string

    :return: String with separator between groups of thousands
    """
    # Convert the number to int or float if it's string
    if isinstance(number, str):
        if ',' in number or '.' in number: # If number is a float
            exit = number.replace(',', '.') # Replace comma to dot if number is in french format
            exit = float(exit)
        else:
            exit = int(number)
    else:
        exit = number       
            
    return '{0:,}'.format(exit).replace(',', ' ')




def remove_borders(image):
    """Remove image borders/white spaces.
    
    :return: croppped image
    """
    try:
        bg = Image.new(image.mode, image.size, (255, 255, 255, 0))
        diff = ImageChops.difference(image, bg)
        diff = ImageChops.add(diff, diff, 2.0, -100)
        bbox = diff.getbbox()
        if bbox:
            return image.crop(bbox)
        else:
            return image
    except:
        return image
    


    
class PDF(FPDF):
    def set_copyright(self,
                  author: str="",
                  creator: str="",
                  title: str="",
                  subject: str="",
                  keywords: str=""):
        """Set copyright to the file.
        
        :param author: The author
        
        :param creator: The creator 
        
        :param author: The author
        
        :param author: The author"""
        super().set_author(author)
        super().set_creator(creator)
        super().set_title(title)
        super().set_subject(subject)
        super().set_producer("PyFPDF/fpdf2 & JCS")
        super().set_keywords(keywords)




    def set_text_color2(self, color: str='black'):
        """Change text color without RGB.
        """
        if color == 'white':
            super().set_text_color(255, 255, 255)  # White text
        if color == 'black':
            super().set_text_color(0, 0, 0)  # Black text





    def center_image(self,
                     image,
                     center_x: int or float=0,
                     center_y: int or float=0,
                     max_width: int or float=1000,
                     max_height: int or float=1000,
                     resizing_percentage: int=0):
        """Add an image to the pdf.
        
        :param image: The image
        
        :param center_x: The X position of the desirate image center
        :type center_x: int or float

        :param center_y: The Y position of the desirate image center
        :type center_y: int or float

        :param max_width: The maximum width of the image
        :type max_width: int or float

        :param max_height: The maximum width of the image
        :type max_height: int or float

        :param resizing_percentage: The resizing percentage to reduce or increase the size
        without changing 'max_height' or 'max_width'
        :type resizing_percentage: int
        
        """
        try:
            r = (100+resizing_percentage)/100
            with Image.open(image) as im:
                wImage, hImage = (im.size)
            X = (max_width / wImage) * r
            if X*hImage > max_height:
                X = (max_height / hImage) * r
            super().image(image, x = center_x - (wImage*X)/2, y = center_y - (hImage*X)/2, w = wImage*X)
            return (wImage*X, hImage*X)
        except Exception as e:
            print(e)
            return