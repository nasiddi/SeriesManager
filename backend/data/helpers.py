from utils import io_utlis
from utils import io_utlis

l = "a and the to in of on with a by or v. at from too en el for vs. as into de la if kHz d'Arthur du x100 unto d'Etat aka und an"
l = l.split(' ')
j = {'part': [], 'lower': [], 'upper': [], 'double': [], 'lower_general': l}

io_utlis.save_json(j, EXCEPTIONS_FILE)
