from app import create_app, db
from app.models import User, Page, Tag, Subscriber, Definition, Link, Product, Record

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 
            'User': User, 
            'Page': Page, 
            'Tag': Tag, 
            'Subscriber': Subscriber,
            'Definition': Definition,
            'Link': Link,
            'Product': Product,
            'Record': Record,
        }
