from database import get_database, COLLECTIONS
from models.testimonial import Testimonial, TestimonialResponse
from models.faq import FAQ, FAQResponse
from typing import List
import logging

logger = logging.getLogger(__name__)

class DataService:
    """Service for managing static content like testimonials and FAQs"""
    
    @staticmethod
    async def get_testimonials() -> List[TestimonialResponse]:
        """Get all active testimonials"""
        try:
            db = get_database()
            cursor = db[COLLECTIONS['testimonials']].find(
                {"is_active": True}
            ).sort("order", 1)
            
            testimonials = []
            async for doc in cursor:
                testimonials.append(TestimonialResponse(**doc))
            
            return testimonials
        except Exception as e:
            logger.error(f"Error fetching testimonials: {e}")
            return []
    
    @staticmethod
    async def get_faqs() -> List[FAQResponse]:
        """Get all active FAQs"""
        try:
            db = get_database()
            cursor = db[COLLECTIONS['faqs']].find(
                {"is_active": True}
            ).sort("order", 1)
            
            faqs = []
            async for doc in cursor:
                faqs.append(FAQResponse(**doc))
            
            return faqs
        except Exception as e:
            logger.error(f"Error fetching FAQs: {e}")
            return []

    @staticmethod
    async def seed_initial_data():
        """Seed database with initial testimonials and FAQs"""
        try:
            db = get_database()
            
            # Seed testimonials
            testimonials_collection = db[COLLECTIONS['testimonials']]
            existing_testimonials = await testimonials_collection.count_documents({})
            
            if existing_testimonials == 0:
                initial_testimonials = [
                    {
                        "id": "1",
                        "text": "Lexi consiguió los primeros 2 pedidos para mi nueva tienda en solo 48 horas. ¡Un comienzo absolutamente increíble para cualquier negocio nuevo!",
                        "author": "Daniel. y",
                        "role": "Nuevo Propietario de Tienda",
                        "rating": 5,
                        "order": 1,
                        "is_active": True
                    },
                    {
                        "id": "2",
                        "text": "Con Lexi, probamos más de 50 libros electrónicos en una sola semana para encontrar nuestros bestsellers. Es la herramienta definitiva para la validación rápida de productos.",
                        "author": "Augon",
                        "role": "Propietario de Tienda de Libros Electrónicos",
                        "rating": 5,
                        "order": 2,
                        "is_active": True
                    }
                ]
                
                await testimonials_collection.insert_many(initial_testimonials)
                logger.info("Seeded testimonials data")
            
            # Seed FAQs
            faqs_collection = db[COLLECTIONS['faqs']]
            existing_faqs = await faqs_collection.count_documents({})
            
            if existing_faqs == 0:
                initial_faqs = [
                    {
                        "id": "1",
                        "question": "¿Qué tipos de productos o servicios puedo promocionar con Lexi?",
                        "answer": "Lexi funciona con una amplia variedad de productos y servicios, desde e-commerce hasta servicios profesionales, educación, SaaS y más. Nuestra IA se adapta automáticamente a tu industria específica.",
                        "category": "general",
                        "order": 1,
                        "is_active": True
                    }
                ]
                
                await faqs_collection.insert_many(initial_faqs)
                logger.info("Seeded FAQs data")
                
        except Exception as e:
            logger.error(f"Error seeding initial data: {e}")
            raise
