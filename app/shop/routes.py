import stripe
from flask import (
        render_template, redirect, url_for, flash, session, request, 
        current_app, make_response, send_from_directory
    )
from app.shop import bp
from sqlalchemy import or_, desc
from app.models import Link, Product, Page
from app import db

@bp.route('/shop')
def index():
    Page.set_nav()
    products = Product.query.filter_by(active=True).order_by('sort','name').all()
    page = Page.query.filter_by(slug='shop').first()
    if products and page:
        return render_template(f'shop/index.html', 
                page=page,
                products=products,
            )
    page = Page.query.filter_by(slug='404-error').first()
    return render_template(f'page/{page.template}.html', page=page)    

@bp.route('/shop/buy/<string:slug>')
def buy(slug):
    product = Product.query.filter_by(slug=slug).first()
    stripe.api_key = current_app.config['STRIPE_SECRET']
    current_app.logger.debug(request.referrer)
    success = (current_app.config['BASE_URL'] +
            url_for('shop.process') +
            '?session_id={CHECKOUT_SESSION_ID}')
    cancel = request.referrer if request.referrer else url_for('shop.view', slug=product.slug)
    current_app.logger.debug(success)
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'name': product.name + " eBook",
            'description': product.description + " Paperback not included.",
            'images': [product.image],
            'amount': product.simple_price(),
            'currency': 'usd',
            'quantity': 1,
        }],
        success_url=success,
        cancel_url=cancel,
    )

    return render_template('shop/buy.html', session=session)

@bp.route('/shop/process-purchase')
def process():
    flash('Thank you for your purchase! Your eBooks will be emailed to you shortly.', 'success')
    return redirect(url_for('shop.index'))



@bp.route('/shop/<string:slug>')
def view(slug):
    Page.set_nav()
    product = Product.query.filter_by(slug=slug,active=True).first()
    page = Page.query.filter_by(slug='shop').first()
    if product:
        if product.active or current_user.is_authenticated:
            related = Product.query.filter(
                    Product.linked_page_id == product.linked_page_id,
                    Product.id != product.id,
                ).order_by('sort','name').limit(4).all()
            page.title = f"Shop: {product.name}"
            price = product.price
            sale_text = ''
            if product.on_sale:
                price = product.sale_price if product.sale_price else product.price
                sale_text = "On Sale! "
            description=f'{sale_text}{product.description} Starting at {price}'
            return render_template(f'shop/view-product.html', 
                    page=page,
                    product=product,
                    related=related,
                    banner=product.image,
                    description=description,
                )
    page = Page.query.filter_by(slug='404-error').first()
    return render_template(f'page/{page.template}.html', page=page)    

@bp.route('/shop/subscribe/<int:obj_id>')
def subscribe(obj_id):
    product = Product.query.filter_by(id=obj_id).first()
    if product:
        flash(f'Please subscribe to receive a copy of <b><i>{product.name}</i></b>.', 'info')
    else:
        flash(f'Please subscribe to receive all subscription downloadables.', 'info')
    return redirect(url_for('page.subscribe'))
