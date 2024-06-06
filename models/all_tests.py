import unittest
import datetime
from models.base_model import BaseModel
from City import City
from Place import Place
from Country import Country
from Amenities import Amenities
from Users import Users
from Review import Review

class TestModels(unittest.TestCase):

    def setUp(self):
        self.user = Users(email="test@example.com", password="password", first_name="John", last_name="Doe")
        self.amenity = Amenities()
        self.amenity.name = "WiFi"
        self.amenity.description = "Free WiFi"
        
        self.city = City()
        self.city.name = "San Francisco"
        self.city.population = 1000000
        self.city.user_id = self.user.id
        
        self.country = Country()
        self.country.name = "USA"
        self.country.population = 330000000
        self.country.city_id = [self.city.id]
        
        self.place = Place(name="Test Place", description="A nice place", address="123 Main St", longitude=-122.4194, latitude=37.7749, price_per_night=100.0, number_of_rooms=3, bathrooms=2, max_guests=6, amenity_id=(self.amenity.id,), city_id=self.city.id, user_id=self.user.id)
        
        self.review = Review()
        self.review.feedback = "Great place!"
        self.review.rating = 5
        self.review.comment = "Had a wonderful time."

    def test_consistency_checks(self):
        now = datetime.datetime.now()
        self.assertIsInstance(self.user.created_at, datetime.datetime)
        self.assertIsInstance(self.user.updated_at, datetime.datetime)
        
        old_updated_at = self.user.updated_at
        self.user.first_name = "Jane"
        self.user.save()
        
        self.assertNotEqual(old_updated_at, self.user.updated_at)
        self.assertGreater(self.user.updated_at, old_updated_at)
    
    def test_relationship_integrity(self):
        self.place.user_id = self.user.id
        self.assertEqual(self.place.user_id, self.user.id)
        
        self.review.place = self.place.id
        self.review.user = self.user.id
        
        self.assertEqual(self.review.place, self.place.id)
        self.assertEqual(self.review.user, self.user.id)
    
    def test_business_rule_enforcement(self):
        another_user = Users(email="another@example.com", password="password", first_name="Jane", last_name="Smith")
        
        with self.assertRaises(ValueError):
            another_place = Place(name="Another Place", description="Another nice place", user_id=self.user.id)
            self.place.user_id = another_user.id
            self.place.save()
    
    def test_user_creation_validation(self):
        with self.assertRaises(ValueError):
            invalid_user = Users(email="invalid_email", password="password", first_name="John", last_name="Doe")
        
        with self.assertRaises(ValueError):
            invalid_user = Users(email="", password="password", first_name="John", last_name="Doe")
    
    def test_unique_email_constraint(self):
        with self.assertRaises(ValueError):
            duplicate_user = Users(email="test@example.com", password="password", first_name="Jane", last_name="Doe")
    
    def test_update_mechanism(self):
        self.user.first_name = "Jane"
        self.user.save()
        
        updated_user = Users(email="test@example.com")
        self.assertEqual(updated_user.first_name, "Jane")
    
    def test_place_instantiation(self):
        with self.assertRaises(ValueError):
            invalid_place = Place(name="", description="Description", address="123 Main St", longitude=-122.4194, latitude=37.7749, price_per_night=100.0, number_of_rooms=3, bathrooms=2, max_guests=6)
        
        valid_place = Place(name="Valid Place", description="Description", address="123 Main St", longitude=-122.4194, latitude=37.7749, price_per_night=100.0, number_of_rooms=3, bathrooms=2, max_guests=6)
        valid_place.save()
    
    def test_host_assignment_rules(self):
        new_host = Users(email="newhost@example.com", password="password", first_name="New", last_name="Host")
        new_host.save()
        
        self.place.user_id = new_host.id
        self.place.save()
        
        self.assertEqual(self.place.user_id, new_host.id)
    
    def test_place_attribute_validation(self):
        with self.assertRaises(ValueError):
            self.place.latitude = 200.0
            self.place.save()
        
        with self.assertRaises(ValueError):
            self.place.price_per_night = -100.0
            self.place.save()
    
    def test_deleting_places(self):
        place_id = self.place.id
        self.place.delete()
        
        with self.assertRaises(ValueError):
            Place.get(place_id)
    
    def test_amenity_addition(self):
        self.place.add_amenity(self.amenity.id)
        self.assertIn(self.amenity.id, self.place.amenity_id)
        
        with self.assertRaises(ValueError):
            self.place.add_amenity(self.amenity.id)
    
    def test_retrieve_and_update_amenities(self):
        amenity_id = self.amenity.id
        self.amenity.name = "Updated WiFi"
        self.amenity.save()
        
        updated_amenity = Amenities.get(amenity_id)
        self.assertEqual(updated_amenity.name, "Updated WiFi")

if __name__ == '__main__':
    unittest.main()
