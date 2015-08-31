from flask_app import app   
from flask import jsonify
        
@app.route('/nutrient/')
def nutrient_index():
    return 'Welcome to nutrient/'

from modules import USDA

@app.route('/nutrient/tags/<string:tags>')
def nutrient_tags(tags):
    '''Computes the nutrient values from entered tags'''

    # Haven't handled spaces and such
    # Use flask.requests inplace of URL
    result = {str('%s %s'%(k[0],k[1])):v for k,v in USDA.id2nut(USDA.tag2id(str(tags))[0]).items()}
    return jsonify(result)
    
    
# Maybe add tag2nut function inside USDA and implement it with default / ones in paper selection settings
# and return in a jsonifiable format i.e. keys = string instead of tuples    