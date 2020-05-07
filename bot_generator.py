"""
Generador de usuarios para la página Silkroad Latino.
"""

from random import sample
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

URL_reg = "https://www.alfa.srolatino-servers.com/register/step/1"
URL_email = "https://10minutemail.net/"

OPTIONS = Options()
OPTIONS.add_argument("--headless")
OPTIONS.add_argument("--window-size=1920x1080")


def random_name():
    """
    Generador aleatorio de valores.
    """

    chars_min = [chr(i) for i in range(97, 123)]
    chars_may = list(map(lambda s: s.upper(), chars_min))
    chars_num = list(map(lambda n: str(n), range(30)))

    chars = chars_min + chars_may + chars_num
    ran_name = sample(chars, 20)
    return "".join(ran_name)

class UserBot:

    def __init__(self, num, pref, pswd=1234):

        self.num = num
        self.pref = pref
        self.pswd = pswd
        self.driver = webdriver.Chrome(options=OPTIONS)

    def switch_to(self, url):
        """
        Cambia el navegador a la url deseada.

        url: URL al cual se quiere ir a navegar.
        """

        self.driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND+'t')
        self.driver.get(url)
        self.driver.implicitly_wait(10)

    def verify_register(self):
        """
        Verifica si el registro después del paso 3 se realizó satisfactoriamente.
        """

        curr_url = self.driver.current_url

        if curr_url == "https://www.alfa.srolatino-servers.com/signin":
            return True

        return False

    def send_email_request(self):
        """
        Realización del paso 1 en el que se genera el email random y se manda
        el correo de verificación.
        """

        # Abre la página donde se genera el email aleatorio.
        self.driver.get("https://10minutemail.net/")
        self.driver.implicitly_wait(10)

        # Obtención del email generado
        webd_email = self.driver.find_element_by_class_name("mailtext")
        email = webd_email.get_attribute("value")

        # Abre en un nuevo tab de la página donde se crea el nuevo usuario.
        self.switch_to(URL_reg)

        id_value = self.pref + "{:04d}".format(self.num)
        inp_list = [id_value, email, self.pswd, self.pswd]

        inputs = self.driver.find_elements_by_tag_name("input")[:7]

        # Rellena los inputs con los valores deseados.
        for i, value in enumerate(inp_list):
            inputs[i].send_keys(value)

        inputs[4].click()

        # Calcula la suma para la verificación del bot.
        operation = inputs[5].get_attribute("placeholder").split()[0]
        result = eval(operation)
        inputs[5].send_keys(result)

        # click en el botón de next.
        btn_next = self.driver.find_element_by_xpath("/html/body/div[1]/div[2]/form/div[8]/button")
        btn_next.click()

        self.driver.implicitly_wait(10)

        # Se va a la página del email para poder verificar luego la cuenta.
        self.switch_to(URL_email)

    def verify_email(self):
        """
        Realización del paso 2 y 3 del registro para finalizar el registro de
        la cuenta.
        """

        # Busca el email para verificar el registro de la cuenta.
        table_mail = self.driver.find_element_by_id("maillist")
        link_ver = table_mail.find_element_by_tag_name("a")
        link_ver.click()
        self.driver.implicitly_wait(10)

        # Cambia al tab de URL para obtener el link para verificar la cuenta.
        url_tab = self.driver.find_element_by_class_name("abgne_tab")
        url_tab.find_elements_by_tag_name("a")[3].click()
        self.driver.implicitly_wait(10)

        # Obtención del url de verificacion.
        div_ver = self.driver.find_element_by_id("tab4")
        url_ver = div_ver.find_element_by_tag_name("a")
        self.switch_to(url_ver.text)

        # Click del botón de verificación en el paso 2.
        btn_next = self.driver.find_element_by_xpath("/html/body/div[1]/div[2]/form/div[2]/button")
        btn_next.click()
        self.driver.implicitly_wait(10)

        # Rellenando los inputs en el paso 3 del registro.
        inputs = self.driver.find_elements_by_tag_name("input")[3:7]
        for i, inp in enumerate(inputs):
            if i == 0:
                inp.send_keys("Nombre")
            else:
                inp.send_keys(random_name())

        # Click en botón para finalizar el paso 3.
        self.driver.find_element_by_xpath("/html/body/div[1]/div[2]/form/div[8]/button").click()
        self.driver.implicitly_wait(10)

        # Verifica si el registro se realizó satisfactoriamente.
        if self.verify_register():
            print("La cuenta número {} ha sido creada".format(self.num))
        else:
            print("La cuenta número {} ha fallado".format(self.num))

        self.driver.quit()

    def kill(self):

        self.driver.quit()

def main():
    "Main function"

    init_num = 21
    last_num = 30
    cases_same_time = 5
    total_it = (last_num-init_num+1) // cases_same_time
    counter = 0

    if (last_num - init_num + 1) % cases_same_time != 0:
        print("Se crearán {} bots".format(total_it*cases_same_time))

    for n in range(total_it):
        bot_list = []

        for i in range(cases_same_time):
            bot_list.append(UserBot(init_num+counter, "mytest"))
            bot_list[i].send_email_request()
            counter += 1

        for bot in bot_list:
            try:
                bot.verify_email()
            except:
                print("La cuenta número {} ha fallado".format(bot.num))
                bot.kill()
                continue

if __name__ == "__main__":
    main()
