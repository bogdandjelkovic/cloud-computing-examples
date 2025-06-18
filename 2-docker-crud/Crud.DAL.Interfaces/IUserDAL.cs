using Crud.Model;

namespace Crud.DAL.Interfaces
{
    public interface IUserDAL
    {
        Task<List<Model.User>> GetAllAsync();
        Task<User> GetByIdAsync(long id);
        Task InsertAsync(User user);
        Task UpdateAsync(User user);
        Task DeleteAsync(User user);
    }
}