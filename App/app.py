from flask import Flask, render_template, request, url_for
from os.path import join, dirname, realpath
import tensorflow as tf
from keras.models import load_model
import numpy as np

app = Flask(__name__)
model = load_model('waste_model.h5')
categories = ['Electronic Waste', 'Glass Waste', 'Metal Waste', 'Organic Waste', 'Paper Waste', 'Plastic Waste', 'Textile Waste']
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
description = {
    'Electronic Waste': 'E-waste, short for electronic waste, refers to discarded electronic devices and equipment that have reached the end of their useful life or are no longer wanted. This includes a wide range of electronic devices such as computers, laptops, smartphones, televisions, printers, cameras, and various household appliances. E-waste contains valuable materials like gold, silver, copper, and palladium, but it also contains hazardous substances like lead, mercury, cadmium, and brominated flame retardants, which can be harmful to human health and the environment if not properly managed.',

    'Glass Waste': 'Glass waste refers to discarded glass products that have reached the end of their useful life or are no longer needed. Glass is a versatile material that is commonly used in various industries and households due to its transparency, durability, and recyclability. Glass waste can include items such as bottles, jars, windows, mirrors, glassware, and packaging materials.',

    'Metal Waste': 'Metal waste refers to discarded metallic materials that have fulfilled their intended purpose or are no longer needed. Metal is a valuable and widely used material in various industries, including construction, manufacturing, automotive, and electronics. Metal waste can encompass a range of items such as scrap metal, metal parts, machinery, appliances, cans, and packaging materials.',

    'Organic Waste': 'Organic waste refers to biodegradable materials that are derived from living organisms or natural processes. It primarily consists of food waste, yard waste, and other biodegradable materials such as paper, cardboard, and untreated wood. Organic waste is highly perishable and can decompose rapidly under suitable conditions.',

    'Paper Waste': 'Paper waste refers to discarded or used paper materials that are no longer needed or have reached the end of their useful life. Paper is one of the most commonly used materials in our daily lives, found in various forms such as office paper, newspapers, magazines, cardboard, packaging materials, and more.',

    'Plastic Waste': 'Plastic waste refers to discarded or used plastic materials that are no longer needed or have completed their intended use. Plastic is a synthetic polymer that is durable, lightweight, and versatile, making it a commonly used material in a wide range of applications. Plastic waste includes items such as plastic bottles, packaging materials, bags, utensils, toys, and various single-use plastic products.',

    'Textile Waste': 'Textile waste refers to discarded or unused textile materials that are no longer needed or have reached the end of their life cycle. It encompasses a wide range of fabrics and textiles, including clothing, bedding, towels, curtains, upholstery, and other fabric-based items. Textile waste can occur due to factors such as changes in fashion trends, wear and tear, damage, or simply the accumulation of unused textiles.'
}

disposal_method = {
    'Electronic Waste': 'To dispose of e-waste, follow these steps: 1) Research local e-waste disposal options and regulations. 2) Locate e-waste recycling centers or authorized collection points near you. 3) Drop off your e-waste at these designated locations for proper recycling. Avoid throwing e-waste in regular trash bins or landfills to prevent environmental harm',

    'Glass Waste': 'To dispose of glass waste responsibly, follow these steps: 1) Separate glass waste from other recyclables. 2) Check with your local waste management authority for recycling options. 3) Look for glass recycling centers or designated collection points in your area. 4) Place glass waste in designated glass recycling bins or containers. 5) If recycling is not available, handle broken glass carefully and dispose of it in puncture-resistant bags labeled as "broken glass." Remember, never put glass waste in regular trash bins or litter it in the environment.',

    'Metal Waste': 'To dispose of metal waste properly, follow these steps: 1) Separate metal waste from other types of waste. 2) Check with your local recycling facilities or waste management authority for metal recycling options. 3) Locate scrap metal collection centers or recycling programs in your area. 4) Prepare metal waste for recycling by cleaning and removing non-metal components if possible. 5) Take the metal waste to the designated recycling centers or schedule pick-up services if available. Avoid disposing of metal waste in regular trash bins or landfills to conserve resources and reduce environmental impact.',

    'Organic Waste': 'To dispose of organic waste in an environmentally-friendly manner, follow these steps: 1) Separate organic waste, such as food scraps and yard trimmings, from other types of waste. 2) Consider composting as a sustainable option. Set up a backyard compost bin or use a composting service if available in your area. 3) If composting is not feasible, check if your community has municipal composting programs or designated collection points for organic waste. 4) Utilize food waste disposers or in-sink composters for smaller food scraps, if permitted in your area. 5) Avoid throwing organic waste in regular trash bins to minimize landfill waste and methane emissions. Responsible disposal of organic waste helps divert valuable resources from landfills and supports the production of nutrient-rich compost for soil health.',

    'Paper Waste': 'To dispose of paper waste responsibly, follow these steps: 1) Separate paper waste from other types of waste for recycling. 2) Check with your local waste management authority for paper recycling guidelines and collection programs in your area. 3) Place paper waste in designated recycling bins or containers. 4) If possible, reduce paper consumption by opting for digital documents and utilizing reusable alternatives. 5) Consider reusing paper when appropriate or repurposing it for crafts or packaging. 6) If recycling options are unavailable, dispose of paper waste in designated trash bins. Avoid contaminating paper waste with non-recyclable materials. By recycling paper waste, we conserve resources, reduce landfill waste, and contribute to a more sustainable approach to paper consumption.',

    'Plastic Waste': 'To dispose of plastic waste responsibly, follow these steps: 1) Separate plastic waste from other types of waste for recycling. 2) Check with your local waste management authority for plastic recycling guidelines and programs in your area. 3) Place plastic waste in designated recycling bins or containers. 4) Reduce plastic consumption by opting for reusable alternatives and avoiding single-use plastics. 5) Properly dispose of plastic bags at designated drop-off locations or recycling centers. 6) Avoid littering or disposing of plastic waste in the environment. 7) Advocate for sustainable practices and support initiatives that promote plastic waste reduction. By recycling and reducing plastic waste, we can minimize environmental pollution, conserve resources, and contribute to a healthier planet.',

    'Textile Waste': 'To dispose of textile waste responsibly, follow these steps: 1) Consider donating or reusing textiles that are still in good condition. Charitable organizations and thrift stores often accept second-hand clothing and textiles. 2) Explore textile recycling programs or drop-off locations in your area. Many communities have initiatives to recycle textiles into new products. 3) Participate in clothing swaps or exchanges to extend the life of textiles and reduce waste. 4) Repurpose or upcycle old textiles for DIY projects or home crafts. 5) If disposal is necessary, check with local waste management authorities for guidelines on proper disposal methods. By responsibly managing textile waste, we can minimize landfill waste, support circular economy practices, and contribute to a more sustainable future.'
}

def allow_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def index_post():
    if 'imagefile' not in request.files:
        return render_template('index.html', prediction='No file selected')
    imagefile = request.files['imagefile']
    if imagefile.filename == '':
        return render_template('index.html', prediction='No file selected')
    if not allow_file(imagefile.filename):
        return render_template('index.html', prediction='Invalid file type')
    UPLOADS_PATH = dirname(realpath(__file__))
    image_path = join(UPLOADS_PATH, 'static', 'uploads', imagefile.filename)
    imagefile.save(image_path)
    img_path = url_for('static', filename='uploads/' + imagefile.filename)
    image = tf.keras.utils.load_img(image_path, target_size=(224, 224))
    image = tf.keras.utils.img_to_array(image)
    image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
    result = np.argmax(model.predict(image), axis = 1)
    prediction = categories[result[0]]
    return render_template('index.html', img = img_path, prediction=prediction, description=description[prediction], disposal = disposal_method[prediction])

if __name__ == '__main__':
    app.run(port = 3000, debug=True)