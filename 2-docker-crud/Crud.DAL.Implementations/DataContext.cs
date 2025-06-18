using Microsoft.EntityFrameworkCore;

namespace Crud.DAL.Implementations
{
    public class DataContext : DbContext
    {
        public DataContext(DbContextOptions<DataContext> options)
            : base(options)
        {
        }

        public DbSet<Model.User> Users { get; set; }
    }
}