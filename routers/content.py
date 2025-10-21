from fastapi import APIRouter, HTTPException
from services.data_service import DataService
from models.testimonial import TestimonialResponse
from models.faq import FAQResponse
from typing import List
import logging

router = APIRouter(prefix="/content", tags=["Content"])
logger = logging.getLogger(__name__)

@router.get("/testimonials", response_model=List[TestimonialResponse])
async def get_testimonials():
    """Get all active testimonials"""
    try:
        from database import get_database, COLLECTIONS
        db = get_database()
        
        # Direct database query for testing
        cursor = db[COLLECTIONS['testimonials']].find({"is_active": True}).sort("order", 1)
        testimonials = []
        
        async for doc in cursor:
            # Clean the document for the response model
            clean_doc = {
                "id": doc.get("id", str(doc.get("_id", ""))),
                "text": doc.get("text", ""),
                "author": doc.get("author", ""),
                "role": doc.get("role", ""),
                "company": doc.get("company"),
                "avatar": doc.get("avatar"),
                "rating": doc.get("rating", 5)
            }
            testimonials.append(TestimonialResponse(**clean_doc))
        
        return testimonials
    except Exception as e:
        logger.error(f"Error fetching testimonials: {e}")
        # Return fallback data
        return [
            TestimonialResponse(
                id="1",
                text="Lexi consiguió los primeros 2 pedidos para mi nueva tienda en solo 48 horas. ¡Un comienzo absolutamente increíble para cualquier negocio nuevo!",
                author="Daniel. y",
                role="Nuevo Propietario de Tienda",
                rating=5
            ),
            TestimonialResponse(
                id="2",
                text="Con Lexi, probamos más de 50 libros electrónicos en una sola semana para encontrar nuestros bestsellers. Es la herramienta definitiva para la validación rápida de productos.",
                author="Augon",
                role="Propietario de Tienda de Libros Electrónicos",
                rating=5
            )
        ]

@router.get("/faq", response_model=List[FAQResponse])
async def get_faqs():
    """Get all active FAQs"""
    try:
        from database import get_database, COLLECTIONS
        db = get_database()
        
        # Direct database query for testing
        cursor = db[COLLECTIONS['faqs']].find({"is_active": True}).sort("order", 1)
        faqs = []
        
        async for doc in cursor:
            # Clean the document for the response model
            clean_doc = {
                "id": doc.get("id", str(doc.get("_id", ""))),
                "question": doc.get("question", ""),
                "answer": doc.get("answer", ""),
                "category": doc.get("category", "general")
            }
            faqs.append(FAQResponse(**clean_doc))
        
        return faqs
    except Exception as e:
        logger.error(f"Error fetching FAQs: {e}")
        # Return fallback data
        return [
            FAQResponse(
                id="1",
                question="¿Qué tipos de productos o servicios puedo promocionar con Lexi?",
                answer="Lexi funciona con una amplia variedad de productos y servicios, desde e-commerce hasta servicios profesionales, educación, SaaS y más. Nuestra IA se adapta automáticamente a tu industria específica.",
                category="general"
            ),
            FAQResponse(
                id="2",
                question="¿Qué países y regiones soporta Lexi?",
                answer="Lexi opera en más de 50 países globalmente, cubriendo todas las principales regiones donde Meta Ads está disponible. Nuestro sistema se adapta automáticamente a las regulaciones locales y mejores prácticas.",
                category="general"
            )
        ]
